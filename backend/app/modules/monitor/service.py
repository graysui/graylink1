from datetime import datetime
import asyncio
from loguru import logger
from .scanner import FileScanner
from .gdrive import GoogleDriveClient
from ...core.config import settings
from typing import Optional, Callable

class MonitorService:
    def __init__(self, db_session, event_callback: Optional[Callable] = None):
        self.db_session = db_session
        self.event_callback = event_callback
        self.scanner = None
        self.is_running = False
        
    async def start(self):
        """启动监控服务"""
        if self.is_running:
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
            
            # 启动监控循环
            asyncio.create_task(self._monitor_loop())
            logger.info("Monitor service started")
            
        except Exception as e:
            logger.error(f"Failed to start monitor service: {str(e)}")
            raise

    async def stop(self):
        """停止监控服务"""
        self.is_running = False
        logger.info("Monitor service stopped")

    async def _monitor_loop(self):
        """监控循环"""
        while self.is_running:
            try:
                # 执行扫描
                changes = await self.scanner.scan_directory(settings.monitor.source_dir)
                
                # 如果有变更且回调函数存在，则调用回调
                if changes and self.event_callback:
                    await self.event_callback(changes)
                    
                # 等待下一次扫描
                await asyncio.sleep(settings.monitor.scan_interval)
                
            except Exception as e:
                logger.error(f"Error in monitor loop: {str(e)}")
                await asyncio.sleep(60)  # 发生错误时等待较短时间后重试 