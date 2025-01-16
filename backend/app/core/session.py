"""会话管理模块

提供数据库会话管理，支持会话生命周期管理和性能监控。
"""
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional, Dict, Any

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import default_cache
from app.core.database import AsyncSessionLocal

class SessionManager:
    """会话管理器
    
    管理数据库会话的生命周期，提供性能监控。
    """
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'SessionManager':
        """获取会话管理器实例（单例）"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        """初始化会话管理器"""
        # 会话统计
        self._active_sessions = 0
        self._total_sessions = 0
        self._failed_sessions = 0
        self._session_times = []  # 记录最近100个会话的时间
        self._last_cleanup = None
        
    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """获取数据库会话
        
        Yields:
            数据库会话
        """
        session = AsyncSessionLocal()
        start_time = time.time()
        self._active_sessions += 1
        self._total_sessions += 1
        
        try:
            yield session
            await session.commit()
            
            # 记录会话时间
            session_time = time.time() - start_time
            self._session_times.append(session_time)
            if len(self._session_times) > 100:
                self._session_times.pop(0)
                
        except SQLAlchemyError as e:
            self._failed_sessions += 1
            await session.rollback()
            logger.error(f"会话错误: {str(e)}")
            raise
            
        finally:
            self._active_sessions -= 1
            await session.close()
            
    def get_stats(self) -> Dict[str, Any]:
        """获取会话统计信息"""
        return {
            "active_sessions": self._active_sessions,
            "total_sessions": self._total_sessions,
            "failed_sessions": self._failed_sessions,
            "avg_session_time": sum(self._session_times) / len(self._session_times) if self._session_times else 0,
            "last_cleanup": self._last_cleanup.isoformat() if self._last_cleanup else None
        } 