from typing import List, Dict, Optional
from loguru import logger
import os
from .client import EmbyClient
from ...core.config import settings

class EmbyService:
    """Emby服务"""

    def __init__(self):
        self.client = EmbyClient()
        self.target_dir = settings.symlink.target_dir

    async def refresh_root(self) -> bool:
        """刷新整个媒体库"""
        try:
            if await self.client.refresh_root_library():
                logger.info("刷新媒体库成功")
                return True
            else:
                logger.error("刷新媒体库失败")
                return False
        except Exception as e:
            logger.error(f"刷新媒体库出错：{str(e)}")
            return False

    def _map_path(self, path: str) -> str:
        """处理路径映射"""
        mapped_path = path
        for local_path, emby_path in settings.emby.path_mapping.items():
            if path.startswith(local_path):
                mapped_path = path.replace(local_path, emby_path, 1)
                break
        return mapped_path

    async def refresh_by_paths(self, paths: List[str]) -> Dict[str, int]:
        """按路径刷新媒体库
        
        Args:
            paths: 需要刷新的路径列表
        """
        success = 0
        failed = 0
        processed = set()

        try:
            # 获取媒体库路径列表
            library_paths = await self.client.get_paths()
            if not library_paths:
                logger.error("未获取到媒体库路径")
                return {"success": 0, "failed": 0}

            # 获取媒体库路径映射
            path_mapping = {
                path["Path"]: path["Locations"][0]
                for path in library_paths
                if path.get("Locations")
            }

            # 处理每个路径
            for path in paths:
                full_path = os.path.join(self.target_dir, path)
                parent_path = os.path.dirname(full_path)
                
                # 应用路径映射
                mapped_path = self._map_path(parent_path)

                # 查找匹配的媒体库路径
                matched_path = None
                for lib_path, real_path in path_mapping.items():
                    if mapped_path.startswith(real_path):
                        matched_path = lib_path
                        break

                if not matched_path or matched_path in processed:
                    continue

                # 刷新匹配的路径
                if await self.client.refresh_library_bypath(matched_path):
                    success += 1
                    processed.add(matched_path)
                    logger.info(f"刷新媒体库路径成功：{matched_path}")
                else:
                    failed += 1
                    logger.error(f"刷新媒体库路径失败：{matched_path}")

            return {
                "success": success,
                "failed": failed,
                "processed": list(processed)
            }

        except Exception as e:
            logger.error(f"按路径刷新媒体库出错：{str(e)}")
            return {"success": success, "failed": failed + 1} 