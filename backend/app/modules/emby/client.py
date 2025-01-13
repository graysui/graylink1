from typing import List, Dict, Optional
import aiohttp
from loguru import logger
from ...core.config import settings

class EmbyClient:
    """Emby API客户端"""

    def __init__(self):
        self.host = settings.emby.host.rstrip('/')
        self.api_key = settings.emby.api_key
        self.headers = {
            'X-Emby-Token': self.api_key,
            'Content-Type': 'application/json'
        }

    async def get_medias(self) -> List[Dict]:
        """获取媒体库列表"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.host}/emby/Library/MediaFolders",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("Items", [])
                    else:
                        logger.error(f"获取媒体库列表失败，错误码：{response.status}")
                        return []
        except Exception as e:
            logger.error(f"获取媒体库列表出错：{str(e)}")
            return []

    async def get_paths(self) -> List[Dict]:
        """获取媒体库路径"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.host}/emby/Library/VirtualFolders",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"获取媒体库路径失败，错误码：{response.status}")
                        return []
        except Exception as e:
            logger.error(f"获取媒体库路径出错：{str(e)}")
            return []

    async def refresh_root_library(self) -> bool:
        """刷新整个媒体库"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.host}/emby/Library/Refresh",
                    headers=self.headers
                ) as response:
                    return response.status == 204
        except Exception as e:
            logger.error(f"刷新媒体库出错：{str(e)}")
            return False

    async def refresh_library_bypath(self, path: str) -> bool:
        """刷新指定路径的媒体库"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.host}/emby/Library/Refresh",
                    params={"Path": path},
                    headers=self.headers
                ) as response:
                    return response.status == 204
        except Exception as e:
            logger.error(f"刷新媒体库路径 {path} 出错：{str(e)}")
            return False 