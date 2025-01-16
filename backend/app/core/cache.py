"""缓存管理模块

提供应用级缓存管理，支持 TTL 缓存、性能监控和缓存策略配置。
"""
import asyncio
import json
import time
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Set, Union

from cachetools import LRUCache, TTLCache
from loguru import logger

from app.core.config import ConfigError, settings

class CacheError(Exception):
    """缓存错误"""
    pass

class CacheStrategy:
    """缓存策略"""
    TTL = "ttl"  # 基于时间的缓存
    LRU = "lru"  # 最近最少使用缓存

class CacheValue:
    """缓存值包装器"""
    
    def __init__(self, value: Any, created_at: datetime = None):
        """初始化缓存值
        
        Args:
            value: 原始值
            created_at: 创建时间
        """
        self.value = value
        self.created_at = created_at or datetime.now()
        self.access_count = 0
        self.last_accessed = None
        
    def access(self):
        """记录访问"""
        self.access_count += 1
        self.last_accessed = datetime.now()
        
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "value": self.value,
            "created_at": self.created_at.isoformat(),
            "access_count": self.access_count,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None
        }

class CacheManager:
    """缓存管理器
    
    提供应用级缓存管理，支持多种缓存策略和性能监控。
    """
    
    _instances: Dict[str, 'CacheManager'] = {}
    
    @classmethod
    def get_instance(
        cls,
        namespace: str = "default",
        **kwargs
    ) -> 'CacheManager':
        """获取缓存实例
        
        Args:
            namespace: 缓存命名空间
            **kwargs: 其他参数
            
        Returns:
            缓存管理器实例
        """
        if namespace not in cls._instances:
            cls._instances[namespace] = cls(namespace=namespace, **kwargs)
        return cls._instances[namespace]
    
    def __init__(
        self,
        strategy: str = CacheStrategy.TTL,
        ttl: int = 300,
        maxsize: int = 1000,
        namespace: str = "default",
        cleanup_interval: int = 3600
    ):
        """初始化缓存管理器
        
        Args:
            strategy: 缓存策略，支持 TTL 和 LRU
            ttl: 缓存过期时间（秒）
            maxsize: 最大缓存条目数
            namespace: 缓存命名空间
            cleanup_interval: 清理间隔（秒）
        """
        if strategy not in (CacheStrategy.TTL, CacheStrategy.LRU):
            raise CacheError(f"不支持的缓存策略: {strategy}")
            
        self.strategy = strategy
        self.namespace = namespace
        self.ttl = ttl
        self.maxsize = maxsize
        self.cleanup_interval = cleanup_interval
        
        self.cache = (
            TTLCache(maxsize=maxsize, ttl=ttl)
            if strategy == CacheStrategy.TTL
            else LRUCache(maxsize=maxsize)
        )
        
        # 性能统计
        self.hits = 0
        self.misses = 0
        self.set_operations = 0
        self.failed_operations = 0
        self._last_cleanup = datetime.now()
        
        # 监控数据
        self._access_times: Dict[str, float] = {}
        self._value_sizes: Dict[str, int] = {}
        self._hot_keys: Set[str] = set()  # 热点键
        self._expired_keys: Set[str] = set()  # 过期键
        
        # 启动清理任务
        asyncio.create_task(self._cleanup_task())
    
    def _get_full_key(self, key: str) -> str:
        """获取完整的缓存键"""
        return f"{self.namespace}:{key}"
    
    def _record_access_time(self, key: str, start_time: float):
        """记录访问时间"""
        access_time = time.time() - start_time
        self._access_times[key] = access_time
        
        # 更新热点键
        if access_time < 0.001:  # 访问时间小于 1ms
            self._hot_keys.add(key)
    
    def _record_value_size(self, key: str, value: Any):
        """记录值大小"""
        try:
            size = len(json.dumps(value)) if isinstance(value, (dict, list)) else len(str(value))
            self._value_sizes[key] = size
            
            # 如果值过大，记录警告
            if size > 1024 * 1024:  # 1MB
                logger.warning(f"缓存值过大 [{key}]: {size} bytes")
        except Exception:
            self._value_sizes[key] = 0
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值
        
        Args:
            key: 缓存键
            
        Returns:
            缓存的值或 None（如果不存在）
        """
        start_time = time.time()
        full_key = self._get_full_key(key)
        
        try:
            cached = self.cache.get(full_key)
            if cached is not None:
                if isinstance(cached, CacheValue):
                    cached.access()
                    value = cached.value
                else:
                    value = cached
                    
                self.hits += 1
                self._record_access_time(full_key, start_time)
                return value
            
            self.misses += 1
            return None
            
        except Exception as e:
            self.failed_operations += 1
            logger.error(f"获取缓存失败 [{full_key}]: {str(e)}")
            return None

    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        track_access: bool = True
    ) -> bool:
        """设置缓存值
        
        Args:
            key: 缓存键
            value: 要缓存的值
            ttl: 可选的过期时间（秒）
            track_access: 是否跟踪访问信息
            
        Returns:
            是否设置成功
        """
        full_key = self._get_full_key(key)
        
        try:
            # 包装缓存值
            if track_access:
                cache_value = CacheValue(value)
                value_to_cache = cache_value
            else:
                value_to_cache = value
            
            if ttl and self.strategy == CacheStrategy.TTL:
                # 创建新的 TTL 缓存用于特定过期时间
                temp_cache = TTLCache(maxsize=1, ttl=ttl)
                temp_cache[full_key] = value_to_cache
                self.cache[full_key] = temp_cache[full_key]
            else:
                self.cache[full_key] = value_to_cache
                
            self.set_operations += 1
            self._record_value_size(full_key, value)
            return True
            
        except Exception as e:
            self.failed_operations += 1
            logger.error(f"设置缓存失败 [{full_key}]: {str(e)}")
            return False

    def invalidate(self, key: str) -> bool:
        """清除指定缓存
        
        Args:
            key: 要清除的缓存键
            
        Returns:
            是否清除成功
        """
        full_key = self._get_full_key(key)
        
        try:
            if full_key in self.cache:
                del self.cache[full_key]
                if full_key in self._access_times:
                    del self._access_times[full_key]
                if full_key in self._value_sizes:
                    del self._value_sizes[full_key]
                self._hot_keys.discard(full_key)
                self._expired_keys.add(full_key)
            return True
            
        except Exception as e:
            self.failed_operations += 1
            logger.error(f"清除缓存失败 [{full_key}]: {str(e)}")
            return False

    def clear(self) -> bool:
        """清除所有缓存"""
        try:
            # 记录所有键为过期
            self._expired_keys.update(self.cache.keys())
            
            # 清除所有数据
            self.cache.clear()
            self._access_times.clear()
            self._value_sizes.clear()
            self._hot_keys.clear()
            
            return True
        except Exception as e:
            logger.error(f"清除所有缓存失败: {str(e)}")
            return False

    def get_stats(self) -> dict:
        """获取缓存统计信息
        
        Returns:
            包含统计信息的字典
        """
        total_ops = self.hits + self.misses
        current_time = datetime.now()
        
        # 计算平均访问时间
        avg_access_time = (
            sum(self._access_times.values()) / len(self._access_times)
            if self._access_times else 0
        )
        
        # 获取最大值大小
        max_value_size = max(self._value_sizes.values()) if self._value_sizes else 0
        
        # 获取热点键信息
        hot_keys = [
            {
                "key": key.split(":", 1)[1],  # 移除命名空间前缀
                "access_time": self._access_times.get(key, 0),
                "size": self._value_sizes.get(key, 0)
            }
            for key in self._hot_keys
        ]
        
        return {
            "namespace": self.namespace,
            "strategy": self.strategy,
            "size": len(self.cache),
            "maxsize": self.cache.maxsize,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": self.hits / total_ops if total_ops > 0 else 0,
            "set_operations": self.set_operations,
            "failed_operations": self.failed_operations,
            "error_rate": self.failed_operations / (self.set_operations + total_ops) if (self.set_operations + total_ops) > 0 else 0,
            "avg_access_time": avg_access_time,
            "total_size": sum(self._value_sizes.values()),
            "max_value_size": max_value_size,
            "hot_keys": hot_keys[:10],  # 只返回前10个热点键
            "expired_keys_count": len(self._expired_keys),
            "last_cleanup": self._last_cleanup.isoformat(),
            "uptime": (current_time - self._last_cleanup).total_seconds()
        }
        
    async def _cleanup_task(self):
        """清理任务"""
        while True:
            try:
                # 等待清理间隔
                await asyncio.sleep(self.cleanup_interval)
                
                # 清理过期数据
                self._last_cleanup = datetime.now()
                expired_time = self._last_cleanup - timedelta(seconds=self.ttl)
                
                # 清理访问时间记录
                for key, access_time in list(self._access_times.items()):
                    if key not in self.cache:
                        del self._access_times[key]
                
                # 清理值大小记录
                for key in list(self._value_sizes.keys()):
                    if key not in self.cache:
                        del self._value_sizes[key]
                
                # 清理热点键
                self._hot_keys = {
                    key for key in self._hot_keys
                    if key in self.cache
                }
                
                # 清理过期键记录
                cutoff_time = datetime.now() - timedelta(days=7)  # 保留7天的记录
                self._expired_keys = {
                    key for key in self._expired_keys
                    if key in self.cache or key in self._access_times
                }
                
                logger.info(f"缓存清理完成 [{self.namespace}]: {len(self.cache)} 个有效键")
                
            except Exception as e:
                logger.error(f"缓存清理失败: {str(e)}")

# 创建默认缓存实例
try:
    default_cache = CacheManager(
        strategy=settings.cache.strategy,
        ttl=settings.cache.default_ttl,
        maxsize=settings.cache.maxsize,
        cleanup_interval=settings.cache.cleanup_interval
    )
except (ConfigError, Exception) as e:
    logger.warning(f"使用默认配置创建缓存: {str(e)}")
    default_cache = CacheManager()

def cached(
    prefix: str = "",
    ttl: Optional[int] = None,
    key_builder: Optional[Callable] = None,
    cache_instance: Optional[CacheManager] = None,
    track_access: bool = True
):
    """缓存装饰器
    
    Args:
        prefix: 缓存键前缀
        ttl: 可选的过期时间（秒）
        key_builder: 可选的缓存键生成函数
        cache_instance: 可选的缓存实例（默认使用全局实例）
        track_access: 是否跟踪访问信息
        
    Returns:
        装饰器函数
    """
    def decorator(func):
        cache_manager = cache_instance or default_cache
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            if key_builder:
                try:
                    cache_key = key_builder(*args, **kwargs)
                except Exception as e:
                    logger.error(f"生成缓存键失败: {str(e)}")
                    return await func(*args, **kwargs)
            else:
                cache_key = f"{prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # 尝试从缓存获取
            cached_value = cache_manager.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # 执行原函数
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                logger.error(f"执行函数失败 [{cache_key}]: {str(e)}")
                raise
            
            # 存入缓存
            cache_manager.set(
                cache_key,
                result,
                ttl=ttl,
                track_access=track_access
            )
            return result
            
        return wrapper
    return decorator 