from typing import Optional, List, Dict
from datetime import datetime, timezone
from loguru import logger
import asyncio
from app.utils.gdrive import GoogleDriveAPI
from app.utils.config import get_config
from .events import DriveChangeEvent

class GoogleDriveMonitor:
    def __init__(self):
        self.config = get_config()
        self.api = GoogleDriveAPI(
            client_id=self.config.monitor.google_drive.client_id,
            client_secret=self.config.monitor.google_drive.client_secret,
            token_file=self.config.monitor.google_drive.token_file
        )
        self.last_check_time = None
        self._running = False
        self._check_interval = self.config.monitor.interval / 1000  # 转换为秒
        self._change_callbacks = []

    def add_change_callback(self, callback):
        """添加变更回调函数"""
        self._change_callbacks.append(callback)

    async def start(self):
        """启动监控"""
        if self._running:
            return
        
        self._running = True
        while self._running:
            try:
                await self._check_changes()
            except Exception as e:
                logger.error(f"检查Google Drive变更时出错: {str(e)}")
            
            await asyncio.sleep(self._check_interval)

    async def stop(self):
        """停止监控"""
        self._running = False

    async def _check_changes(self):
        """检查文件变更"""
        try:
            changes = self.api.get_changes(self.last_check_time)
            if changes:
                for change in changes:
                    event = DriveChangeEvent(
                        file_id=change.get('id'),
                        file_name=change.get('name'),
                        mime_type=change.get('mimeType'),
                        modified_time=change.get('modifiedTime')
                    )
                    # 触发所有回调
                    for callback in self._change_callbacks:
                        try:
                            await callback(event)
                        except Exception as e:
                            logger.error(f"处理变更回调时出错: {str(e)}")

            self.last_check_time = datetime.now(timezone.utc)
            
        except Exception as e:
            logger.error(f"获取Google Drive变更时出错: {str(e)}")

    def get_auth_url(self) -> str:
        """获取授权URL"""
        return self.api.get_auth_url()

    def authorize_with_code(self, code: str) -> bool:
        """使用授权码完成授权"""
        return self.api.authorize_with_code(code)

    def list_files(self, folder_id: Optional[str] = None) -> List[Dict]:
        """列出文件"""
        return self.api.list_files(folder_id) 