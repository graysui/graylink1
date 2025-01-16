"""监控服务模块

提供文件监控服务，管理扫描任务和事件处理。
"""
from datetime import datetime
import asyncio
from typing import Optional, Callable, Dict, List
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from .scanner import FileScanner
from .gdrive import GoogleDriveClient
from .events import FileChangeHandler
from app.core.config import settings
from app.core.cache import cached

class MonitorService:
    """监控服务
    
    管理文件监控任务，包括扫描调度和事件处理。
    """
    
    def __init__(
        self,
        db_session: AsyncSession,
        event_callback: Optional[Callable] = None,
        max_retries: int = 3,
        retry_delay: int = 60
    ):
        """初始化监控服务
        
        Args:
            db_session: 数据库会话
            event_callback: 事件回调函数
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）
        """
        self.db_session = db_session
        self.event_callback = event_callback
        self.scanner = None
        self.is_running = False
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # 监控统计
        self._start_time = None
        self._total_scans = 0
        self._failed_scans = 0
        self._last_error = None
        self._last_scan_time = None
        self._current_retry_count = 0
        
    @property
    def stats(self) -> Dict:
        """获取监控统计信息"""
        return {
            "status": "running" if self.is_running else "stopped",
            "uptime": (datetime.now() - self._start_time).total_seconds() if self._start_time else 0,
            "total_scans": self._total_scans,
            "failed_scans": self._failed_scans,
            "success_rate": (self._total_scans - self._failed_scans) / self._total_scans if self._total_scans > 0 else 0,
            "last_error": str(self._last_error) if self._last_error else None,
            "last_scan_time": self._last_scan_time.isoformat() if self._last_scan_time else None,
            "scanner_stats": self.scanner.stats if self.scanner else None
        }
        
    async def start(self):
        """启动监控服务"""
        if self.is_running:
            logger.warning("监控服务已在运行中")
            return
            
        try:
            # 初始化Google Drive客户端
            gdrive_client = GoogleDriveClient(
                settings.monitor.google_drive.client_id,
                settings.monitor.google_drive.client_secret,
                settings.monitor.google_drive.token_file
            )
            await gdrive_client.authenticate()
            
            # 初始化扫描器
            self.scanner = FileScanner(self.db_session, gdrive_client)
            self.is_running = True
            self._start_time = datetime.now()
            
            # 启动监控循环
            asyncio.create_task(self._monitor_loop())
            logger.info("监控服务已启动")
            
        except Exception as e:
            logger.error(f"启动监控服务失败: {str(e)}")
            self._last_error = e
            raise

    async def stop(self):
        """停止监控服务"""
        self.is_running = False
        logger.info("监控服务已停止")

    @cached(prefix="monitor_service", ttl=300)
    async def get_monitored_paths(self) -> List[str]:
        """获取所有被监控的路径"""
        try:
            result = await self.db_session.execute(
                select(FileRecord.path).distinct()
            )
            return [path for path, in result.fetchall()]
        except Exception as e:
            logger.error(f"获取监控路径失败: {str(e)}")
            return []

    async def _monitor_loop(self):
        """监控循环"""
        while self.is_running:
            try:
                self._total_scans += 1
                self._last_scan_time = datetime.now()
                
                # 执行扫描
                changes = await self.scanner.scan_directory(settings.monitor.source_dir)
                
                # 如果有变更且回调函数存在，则调用回调
                if changes and self.event_callback:
                    try:
                        await self.event_callback(changes)
                    except Exception as e:
                        logger.error(f"处理变更回调失败: {str(e)}")
                
                # 重置重试计数
                self._current_retry_count = 0
                self._last_error = None
                    
                # 等待下一次扫描
                await asyncio.sleep(settings.monitor.scan_interval)
                
            except Exception as e:
                self._failed_scans += 1
                self._last_error = e
                logger.error(f"监控循环出错: {str(e)}")
                
                # 处理重试逻辑
                if self._current_retry_count < self.max_retries:
                    self._current_retry_count += 1
                    retry_time = self.retry_delay * self._current_retry_count
                    logger.info(f"将在 {retry_time} 秒后重试（第 {self._current_retry_count} 次）")
                    await asyncio.sleep(retry_time)
                else:
                    logger.error("达到最大重试次数，停止监控服务")
                    await self.stop()
                    break 