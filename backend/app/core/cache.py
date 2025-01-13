from typing import Any, Optional
import time
from functools import wraps
from cachetools import TTLCache
from loguru import logger

class CacheManager:
    """缓存管理器"""
    
    def __init__(self, ttl: int = 300, maxsize: int = 100):
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        try:
            value = self.cache.get(key)
            if value is not None:
                self.hits += 1
            else:
                self.misses += 1
            return value
        except Exception as e:
            logger.error(f"获取缓存失败: {str(e)}")
            return None

    def set(self, key: str, value: Any) -> bool:
        """设置缓存值"""
        try:
            self.cache[key] = value
            return True
        except Exception as e:
            logger.error(f"设置缓存失败: {str(e)}")
            return False

    def invalidate(self, key: str) -> bool:
        """清除指定缓存"""
        try:
            if key in self.cache:
                del self.cache[key]
            return True
        except Exception as e:
            logger.error(f"清除缓存失败: {str(e)}")
            return False

    def get_stats(self) -> dict:
        """获取缓存统计信息"""
        return {
            "size": len(self.cache),
            "maxsize": self.cache.maxsize,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0
        }

# 创建全局缓存实例
cache = CacheManager()

def cached(prefix: str = "", ttl: int = 300):
    """缓存装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # 尝试从缓存获取
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # 执行原函数
            result = await func(*args, **kwargs)
            
            # 存入缓存
            cache.set(cache_key, result)
            return result
        return wrapper
    return decorator 