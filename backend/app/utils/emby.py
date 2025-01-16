"""Emby 客户端工具模块

提供与 Emby 服务器交互的基础功能。
"""
import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, List, Any
from loguru import logger

class EmbyError(Exception):
    """Emby 操作异常"""
    pass

class EmbyClient:
    """Emby 基础客户端
    
    提供与 Emby 服务器交互的基础功能。
    """
    
    def __init__(
        self,
        server_url: str,
        api_key: str,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: int = 5
    ):
        """初始化客户端
        
        Args:
            server_url: Emby 服务器地址
            api_key: API 密钥
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）
        """
        self.server_url = server_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # 性能统计
        self._request_count = 0
        self._failed_requests = 0
        self._last_request_time = None
        self._last_error = None
        
    @property
    def stats(self) -> Dict:
        """获取客户端统计信息"""
        return {
            "total_requests": self._request_count,
            "failed_requests": self._failed_requests,
            "success_rate": (self._request_count - self._failed_requests) / self._request_count if self._request_count > 0 else 0,
            "last_request_time": self._last_request_time.isoformat() if self._last_request_time else None,
            "last_error": str(self._last_error) if self._last_error else None
        }
        
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Any:
        """发送 HTTP 请求
        
        Args:
            method: HTTP 方法
            endpoint: API 端点
            **kwargs: 请求参数
            
        Returns:
            响应数据
            
        Raises:
            EmbyError: 请求失败
        """
        url = f"{self.server_url}/{endpoint.lstrip('/')}"
        headers = {
            'X-Emby-Token': self.api_key,
            'Content-Type': 'application/json'
        }
        
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers
        
        self._request_count += 1
        self._last_request_time = datetime.now()
        
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.request(
                        method,
                        url,
                        timeout=aiohttp.ClientTimeout(total=self.timeout),
                        **kwargs
                    ) as response:
                        if response.status in (200, 204):
                            if response.status == 204:
                                return None
                            return await response.json()
                            
                        error_msg = f"请求失败: {response.status}"
                        try:
                            error_data = await response.json()
                            if 'error' in error_data:
                                error_msg = f"{error_msg} - {error_data['error']}"
                        except:
                            pass
                            
                        raise EmbyError(error_msg)
                        
            except asyncio.TimeoutError:
                error_msg = f"请求超时 (尝试 {attempt + 1}/{self.max_retries})"
                logger.warning(error_msg)
                if attempt == self.max_retries - 1:
                    self._failed_requests += 1
                    self._last_error = error_msg
                    raise EmbyError(error_msg)
                await asyncio.sleep(self.retry_delay)
                
            except Exception as e:
                error_msg = f"请求出错: {str(e)}"
                logger.error(error_msg)
                if attempt == self.max_retries - 1:
                    self._failed_requests += 1
                    self._last_error = error_msg
                    raise EmbyError(error_msg)
                await asyncio.sleep(self.retry_delay)
                
    async def refresh_library(self, path: Optional[str] = None) -> bool:
        """刷新媒体库
        
        Args:
            path: 可选的指定路径
            
        Returns:
            是否刷新成功
        """
        try:
            if path:
                # 刷新指定路径
                await self._make_request(
                    'POST',
                    '/Library/Media/Updated',
                    json={'Path': path}
                )
            else:
                # 刷新整个库
                await self._make_request(
                    'POST',
                    '/Library/Refresh'
                )
            return True
            
        except Exception as e:
            logger.error(f"刷新媒体库失败: {str(e)}")
            return False
            
    async def get_server_info(self) -> Optional[Dict]:
        """获取服务器信息"""
        try:
            return await self._make_request('GET', '/System/Info')
        except Exception as e:
            logger.error(f"获取服务器信息失败: {str(e)}")
            return None
            
    async def get_items(
        self,
        parent_id: Optional[str] = None,
        include_item_types: Optional[List[str]] = None,
        recursive: bool = False,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """获取媒体项
        
        Args:
            parent_id: 父项ID
            include_item_types: 包含的项类型
            recursive: 是否递归获取
            sort_by: 排序字段
            sort_order: 排序顺序
            limit: 限制数量
            
        Returns:
            媒体项列表
        """
        try:
            params = {
                'ParentId': parent_id,
                'IncludeItemTypes': ','.join(include_item_types) if include_item_types else None,
                'Recursive': str(recursive).lower(),
                'SortBy': sort_by,
                'SortOrder': sort_order,
                'Limit': limit
            }
            params = {k: v for k, v in params.items() if v is not None}
            
            result = await self._make_request('GET', '/Items', params=params)
            return result.get('Items', [])
            
        except Exception as e:
            logger.error(f"获取媒体项失败: {str(e)}")
            return []
            
    async def get_item(self, item_id: str) -> Optional[Dict]:
        """获取指定媒体项
        
        Args:
            item_id: 媒体项ID
            
        Returns:
            媒体项信息
        """
        try:
            return await self._make_request('GET', f'/Items/{item_id}')
        except Exception as e:
            logger.error(f"获取媒体项失败 [{item_id}]: {str(e)}")
            return None 