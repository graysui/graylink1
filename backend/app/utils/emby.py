import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class EmbyClient:
    def __init__(self, server_url: str, api_key: str):
        self.server_url = server_url.rstrip('/')
        self.api_key = api_key
        
    def refresh_library(self, path: Optional[str] = None) -> bool:
        """
        刷新Emby媒体库
        """
        try:
            headers = {
                'X-Emby-Token': self.api_key
            }
            
            if path:
                # 刷新指定路径
                url = f"{self.server_url}/Library/Media/Updated"
                response = requests.post(url, headers=headers, json={'Path': path})
            else:
                # 刷新整个库
                url = f"{self.server_url}/Library/Refresh"
                response = requests.post(url, headers=headers)
                
            return response.status_code == 204
            
        except Exception as e:
            logger.error(f"刷新Emby媒体库失败: {str(e)}")
            return False 