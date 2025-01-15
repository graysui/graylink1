from typing import List, Dict, Optional
import aiohttp
from loguru import logger
from app.utils.emby import EmbyClient as BaseEmbyClient
from app.utils.config import get_config

class EmbyClient(BaseEmbyClient):
    """扩展的Emby客户端"""

    def __init__(self):
        config = get_config()
        super().__init__(config.emby.server, config.emby.api_key)
        
    async def get_libraries(self) -> List[Dict]:
        """获取媒体库列表"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.server_url}/Library/MediaFolders",
                    headers={'X-Emby-Token': self.api_key}
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("Items", [])
                    else:
                        logger.error(f"获取媒体库列表失败: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"获取媒体库列表出错: {str(e)}")
            return []
            
    async def refresh_by_path(self, path: str) -> bool:
        """刷新指定路径的媒体库"""
        try:
            return await self.refresh_library(path)
        except Exception as e:
            logger.error(f"刷新媒体库路径失败: {str(e)}")
            return False
            
    async def refresh_all(self) -> bool:
        """刷新所有媒体库"""
        try:
            return await self.refresh_library()
        except Exception as e:
            logger.error(f"刷新所有媒体库失败: {str(e)}")
            return False
            
    async def test_connection(self) -> bool:
        """测试连接"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.server_url}/System/Info",
                    headers={'X-Emby-Token': self.api_key}
                ) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"测试Emby连接失败: {str(e)}")
            return False 