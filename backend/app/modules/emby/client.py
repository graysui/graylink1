"""Emby 客户端模块

提供与 Emby 服务器交互的功能实现。
"""
from typing import Optional, Dict, List
from loguru import logger

from app.utils.emby import EmbyClient, EmbyError
from app.core.config import EmbyConfig

class EmbyServiceClient(EmbyClient):
    """Emby 服务客户端
    
    扩展基础客户端，提供更多业务相关的功能。
    """
    
    def __init__(self, config: EmbyConfig):
        """初始化客户端
        
        Args:
            config: Emby 配置
        """
        super().__init__(
            server_url=config.server_url,
            api_key=config.api_key,
            timeout=config.timeout or 30,
            max_retries=config.max_retries or 3,
            retry_delay=config.retry_delay or 5
        )
        self.config = config
        
    async def get_libraries(self) -> List[Dict]:
        """获取所有媒体库
        
        Returns:
            媒体库列表
        """
        try:
            items = await self.get_items(
                include_item_types=['CollectionFolder']
            )
            return [{
                'id': item['Id'],
                'name': item['Name'],
                'type': item.get('CollectionType', 'unknown'),
                'path': item.get('Path', ''),
                'item_count': item.get('ChildCount', 0)
            } for item in items]
            
        except Exception as e:
            logger.error(f"获取媒体库列表失败: {str(e)}")
            return []
            
    async def refresh_by_path(self, path: str) -> bool:
        """刷新指定路径的媒体
        
        Args:
            path: 媒体路径
            
        Returns:
            是否刷新成功
        """
        try:
            # 检查路径是否在配置的媒体库路径中
            path = path.replace('\\', '/')
            valid = any(
                path.startswith(lib_path.replace('\\', '/'))
                for lib_path in self.config.library_paths
            )
            if not valid:
                logger.warning(f"路径不在配置的媒体库中: {path}")
                return False
                
            return await self.refresh_library(path)
            
        except Exception as e:
            logger.error(f"刷新媒体路径失败 [{path}]: {str(e)}")
            return False
            
    async def refresh_all(self) -> bool:
        """刷新所有媒体库
        
        Returns:
            是否刷新成功
        """
        try:
            return await self.refresh_library()
        except Exception as e:
            logger.error(f"刷新所有媒体库失败: {str(e)}")
            return False
            
    async def test_connection(self) -> bool:
        """测试服务器连接
        
        Returns:
            是否连接成功
        """
        try:
            info = await self.get_server_info()
            return bool(info and info.get('Version'))
        except Exception as e:
            logger.error(f"测试服务器连接失败: {str(e)}")
            return False
            
    async def get_library_items(
        self,
        library_id: str,
        item_type: Optional[str] = None,
        sort_by: str = 'DateCreated',
        sort_order: str = 'Descending',
        limit: Optional[int] = None
    ) -> List[Dict]:
        """获取媒体库中的项目
        
        Args:
            library_id: 媒体库ID
            item_type: 项目类型
            sort_by: 排序字段
            sort_order: 排序顺序
            limit: 限制数量
            
        Returns:
            媒体项列表
        """
        try:
            items = await self.get_items(
                parent_id=library_id,
                include_item_types=[item_type] if item_type else None,
                recursive=True,
                sort_by=sort_by,
                sort_order=sort_order,
                limit=limit
            )
            return [{
                'id': item['Id'],
                'name': item['Name'],
                'type': item.get('Type', 'unknown'),
                'path': item.get('Path', ''),
                'created': item.get('DateCreated'),
                'modified': item.get('DateModified'),
                'size': item.get('Size'),
                'played': item.get('PlayCount', 0),
                'last_played': item.get('LastPlayedDate')
            } for item in items]
            
        except Exception as e:
            logger.error(f"获取媒体库项目失败 [{library_id}]: {str(e)}")
            return []
            
    async def get_item_details(self, item_id: str) -> Optional[Dict]:
        """获取媒体项详细信息
        
        Args:
            item_id: 媒体项ID
            
        Returns:
            媒体项详细信息
        """
        try:
            item = await self.get_item(item_id)
            if not item:
                return None
                
            return {
                'id': item['Id'],
                'name': item['Name'],
                'type': item.get('Type', 'unknown'),
                'path': item.get('Path', ''),
                'created': item.get('DateCreated'),
                'modified': item.get('DateModified'),
                'size': item.get('Size'),
                'played': item.get('PlayCount', 0),
                'last_played': item.get('LastPlayedDate'),
                'overview': item.get('Overview'),
                'genres': item.get('Genres', []),
                'tags': item.get('Tags', []),
                'rating': item.get('CommunityRating'),
                'year': item.get('ProductionYear'),
                'duration': item.get('RunTimeTicks'),
                'media_info': item.get('MediaSources', [])
            }
            
        except Exception as e:
            logger.error(f"获取媒体项详情失败 [{item_id}]: {str(e)}")
            return None 