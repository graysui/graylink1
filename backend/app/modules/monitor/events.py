"""事件处理模块

提供文件变更事件的处理和分发功能。
"""
from typing import List, Dict, Optional
from datetime import datetime
import asyncio
from collections import defaultdict
from loguru import logger

from ..symlink.manager import SymlinkManager
from ..emby.service import EmbyService
from app.core.config import settings
from app.core.cache import cached

class FileChangeHandler:
    """文件变更处理器
    
    处理文件系统变更事件，包括创建、修改和删除。
    """
    
    def __init__(self, batch_size: int = 10, batch_interval: float = 1.0):
        """初始化变更处理器
        
        Args:
            batch_size: 批处理大小
            batch_interval: 批处理间隔（秒）
        """
        self.symlink_manager = SymlinkManager()
        self.emby_service = EmbyService()
        self.changed_paths = []  # 记录变更的路径
        
        # 批处理配置
        self.batch_size = batch_size
        self.batch_interval = batch_interval
        
        # 事件队列
        self._event_queue = asyncio.Queue()
        self._is_processing = False
        self._current_batch = defaultdict(list)
        
        # 统计信息
        self._total_events = 0
        self._processed_events = 0
        self._failed_events = 0
        self._last_batch_time = None
        self._last_error = None
        
    @property
    def stats(self) -> Dict:
        """获取处理器统计信息"""
        return {
            "total_events": self._total_events,
            "processed_events": self._processed_events,
            "failed_events": self._failed_events,
            "success_rate": self._processed_events / self._total_events if self._total_events > 0 else 0,
            "pending_events": self._event_queue.qsize(),
            "last_batch_time": self._last_batch_time.isoformat() if self._last_batch_time else None,
            "last_error": str(self._last_error) if self._last_error else None
        }

    async def handle_changes(self, changes: List[Dict]):
        """处理文件变更事件
        
        Args:
            changes: 变更列表
        """
        self._total_events += len(changes)
        
        # 将变更事件加入队列
        for change in changes:
            await self._event_queue.put(change)
        
        # 如果处理器未运行，启动它
        if not self._is_processing:
            self._is_processing = True
            asyncio.create_task(self._process_events())

    async def _process_events(self):
        """处理事件队列"""
        while self._is_processing:
            try:
                # 收集一批事件
                batch = await self._collect_batch()
                if not batch:
                    continue
                
                self._last_batch_time = datetime.now()
                
                # 按类型分组处理
                for event_type, events in batch.items():
                    try:
                        if event_type == 'added':
                            await self._handle_batch_add(events)
                        elif event_type == 'modified':
                            await self._handle_batch_modify(events)
                        elif event_type == 'deleted':
                            await self._handle_batch_delete(events)
                    except Exception as e:
                        logger.error(f"批处理事件失败 [{event_type}]: {str(e)}")
                        self._failed_events += len(events)
                        self._last_error = e
                        continue
                
                # 批量刷新 Emby
                if self.changed_paths:
                    await self._refresh_emby()
                    self.changed_paths = []  # 清空变更路径列表
                
            except Exception as e:
                logger.error(f"处理事件队列出错: {str(e)}")
                self._last_error = e
                await asyncio.sleep(1)  # 发生错误时短暂等待

    async def _collect_batch(self) -> Dict[str, List[Dict]]:
        """收集一批事件
        
        Returns:
            按类型分组的事件批次
        """
        batch = defaultdict(list)
        try:
            for _ in range(self.batch_size):
                try:
                    event = await asyncio.wait_for(
                        self._event_queue.get(),
                        timeout=self.batch_interval
                    )
                    batch[event['type']].append(event['file'])
                    self._event_queue.task_done()
                except asyncio.TimeoutError:
                    break
        except Exception as e:
            logger.error(f"收集事件批次失败: {str(e)}")
        
        return batch

    @cached(prefix="event_handler", ttl=60)
    async def _handle_batch_add(self, files: List[Dict]):
        """批量处理添加事件
        
        Args:
            files: 文件信息列表
        """
        for file in files:
            try:
                if await self.symlink_manager.create_symlink(file['name']):
                    self.changed_paths.append(file['name'])
                    self._processed_events += 1
            except Exception as e:
                logger.error(f"处理文件添加失败 [{file['name']}]: {str(e)}")
                self._failed_events += 1

    async def _handle_batch_modify(self, files: List[Dict]):
        """批量处理修改事件
        
        Args:
            files: 文件信息列表
        """
        for file in files:
            try:
                # 软链接不需要特殊处理，但需要刷新 Emby
                self.changed_paths.append(file['name'])
                self._processed_events += 1
            except Exception as e:
                logger.error(f"处理文件修改失败 [{file['name']}]: {str(e)}")
                self._failed_events += 1

    async def _handle_batch_delete(self, files: List[Dict]):
        """批量处理删除事件
        
        Args:
            files: 文件信息列表
        """
        for file in files:
            try:
                if await self.symlink_manager.remove_symlink(file['path']):
                    self.changed_paths.append(file['path'])
                    self._processed_events += 1
            except Exception as e:
                logger.error(f"处理文件删除失败 [{file['path']}]: {str(e)}")
                self._failed_events += 1

    async def _refresh_emby(self):
        """刷新 Emby 媒体库"""
        try:
            result = await self.emby_service.refresh_by_paths(self.changed_paths)
            logger.info(f"Emby刷新结果：成功{result['success']}个，失败{result['failed']}个")
            if result['processed']:
                logger.info(f"处理的媒体库路径：{', '.join(result['processed'])}")
        except Exception as e:
            logger.error(f"刷新Emby出错: {str(e)}")
            self._last_error = e 