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
    
    提供文件监控服务，管理扫描任务和事件处理。
    支持本地文件和 Google Drive 文件的监控。
    """
    
    def __init__(
        self,
        scanner: FileScanner,
        drive_client: Optional[GoogleDriveClient] = None,
        event_callback: Optional[Callable] = None,
        max_retries: int = 3,
        retry_delay: int = 5
    ):
        """初始化服务
        
        Args:
            scanner: 文件扫描器
            drive_client: Google Drive 客户端
            event_callback: 事件回调函数
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）
        """
        self.scanner = scanner
        self.drive_client = drive_client
        self.event_callback = event_callback
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # 服务状态
        self.is_running = False
        self._monitor_task = None
        self._current_retry_count = 0
        self._total_scans = 0
        self._failed_scans = 0
        self._last_scan_time = None
        self._last_error = None
        
    async def start(self):
        """启动监控服务"""
        if self.is_running:
            logger.warning("监控服务已在运行")
            return
            
        # 如果配置了 Google Drive，确保客户端已认证
        if self.drive_client:
            try:
                await self.drive_client.authenticate()
                logger.info("Google Drive 认证成功")
            except Exception as e:
                logger.error(f"Google Drive 认证失败: {str(e)}")
                raise
            
        self.is_running = True
        self._monitor_task = asyncio.create_task(self._monitor_loop())
        logger.info("监控服务已启动")
        
    async def stop(self):
        """停止监控服务"""
        if not self.is_running:
            logger.warning("监控服务未运行")
            return
            
        self.is_running = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
            self._monitor_task = None
            
        logger.info("监控服务已停止")
        
    @property
    def stats(self) -> Dict:
        """获取服务统计信息"""
        stats = {
            "is_running": self.is_running,
            "total_scans": self._total_scans,
            "failed_scans": self._failed_scans,
            "last_scan_time": self._last_scan_time.isoformat() if self._last_scan_time else None,
            "current_retry_count": self._current_retry_count,
            "last_error": str(self._last_error) if self._last_error else None,
            "scanner_stats": self.scanner.stats if hasattr(self.scanner, 'stats') else None,
            "drive_enabled": self.drive_client is not None
        }
        
        # 如果启用了 Google Drive，添加相关统计
        if self.drive_client:
            stats["drive_stats"] = self.drive_client.stats
            
        return stats
        
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