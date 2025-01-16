"""Emby 服务模块

提供 Emby 服务相关功能。
"""
from typing import Optional, Dict, List
from datetime import datetime
from loguru import logger

from app.core.config import EmbyConfig
from app.modules.emby.client import EmbyServiceClient

class EmbyService:
    """Emby 服务
    
    提供 Emby 服务相关功能的实现。
    """
    
    def __init__(self, config: EmbyConfig):
        """初始化服务
        
        Args:
            config: Emby 配置
        """
        self.config = config
        self.client = EmbyServiceClient(config) if config.api_key else None
        
        # 服务状态
        self._is_ready = False
        self._last_check = None
        self._error_count = 0
        self._last_error = None
        
    @property
    def is_ready(self) -> bool:
        """服务是否就绪"""
        return self._is_ready
        
    @property
    def is_enabled(self) -> bool:
        """服务是否启用"""
        return self.client is not None
        
    @property
    def stats(self) -> Dict:
        """获取服务统计信息"""
        return {
            "is_enabled": self.is_enabled,
            "is_ready": self._is_ready,
            "last_check": self._last_check.isoformat() if self._last_check else None,
            "error_count": self._error_count,
            "last_error": str(self._last_error) if self._last_error else None,
            "client_stats": self.client.stats if self.client else None
        }
        
    async def initialize(self) -> bool:
        """初始化服务
        
        Returns:
            是否初始化成功
        """
        try:
            self._last_check = datetime.now()
            
            # 如果服务未启用，直接返回成功
            if not self.is_enabled:
                logger.info("Emby 服务未启用（未配置 API 密钥）")
                self._is_ready = True
                return True
                
            # 测试连接
            if not await self.client.test_connection():
                self._error_count += 1
                self._last_error = "服务器连接失败"
                self._is_ready = False
                return False
                
            # 获取媒体库列表
            libraries = await self.client.get_libraries()
            if not libraries:
                self._error_count += 1
                self._last_error = "获取媒体库列表失败"
                self._is_ready = False
                return False
                
            # 验证媒体库路径
            valid_paths = set()
            for lib in libraries:
                if lib.get('path'):
                    valid_paths.add(lib['path'].replace('\\', '/'))
                    
            for path in self.config.library_paths:
                path = path.replace('\\', '/')
                if not any(path.startswith(vp) for vp in valid_paths):
                    logger.warning(f"配置的媒体库路径不存在: {path}")
                    
            self._is_ready = True
            self._last_error = None
            return True
            
        except Exception as e:
            self._error_count += 1
            self._last_error = str(e)
            self._is_ready = False
            logger.error(f"初始化 Emby 服务失败: {str(e)}")
            return False
            
    async def refresh_media(self, path: Optional[str] = None) -> bool:
        """刷新媒体
        
        Args:
            path: 可选的指定路径
            
        Returns:
            是否刷新成功
        """
        # 如果服务未启用，直接返回成功
        if not self.is_enabled:
            logger.info("Emby 服务未启用，跳过媒体刷新")
            return True
            
        try:
            if path:
                return await self.client.refresh_by_path(path)
            else:
                return await self.client.refresh_all()
                
        except Exception as e:
            self._error_count += 1
            self._last_error = str(e)
            logger.error(f"刷新媒体失败: {str(e)}")
            return False
            
    async def get_libraries(self) -> List[Dict]:
        """获取媒体库列表
        
        Returns:
            媒体库列表
        """
        if not self._is_ready:
            logger.warning("Emby 服务未就绪")
            return []
            
        try:
            return await self.client.get_libraries()
        except Exception as e:
            self._error_count += 1
            self._last_error = str(e)
            logger.error(f"获取媒体库列表失败: {str(e)}")
            return []
            
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
        if not self._is_ready:
            logger.warning("Emby 服务未就绪")
            return []
            
        try:
            return await self.client.get_library_items(
                library_id=library_id,
                item_type=item_type,
                sort_by=sort_by,
                sort_order=sort_order,
                limit=limit
            )
        except Exception as e:
            self._error_count += 1
            self._last_error = str(e)
            logger.error(f"获取媒体库项目失败: {str(e)}")
            return []
            
    async def get_item_details(self, item_id: str) -> Optional[Dict]:
        """获取媒体项详细信息
        
        Args:
            item_id: 媒体项ID
            
        Returns:
            媒体项详细信息
        """
        if not self._is_ready:
            logger.warning("Emby 服务未就绪")
            return None
            
        try:
            return await self.client.get_item_details(item_id)
        except Exception as e:
            self._error_count += 1
            self._last_error = str(e)
            logger.error(f"获取媒体项详情失败: {str(e)}")
            return None 