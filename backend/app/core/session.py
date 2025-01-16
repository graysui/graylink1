"""会话管理模块

提供数据库会话管理，支持会话生命周期管理和性能监控。
"""
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import cache
from app.core.database import AsyncSessionLocal

class SessionManager:
    """会话管理器
    
    提供数据库会话的生命周期管理和性能监控。
    """
    
    def __init__(self):
        """初始化会话管理器"""
        self.active_sessions = 0
        self.total_sessions = 0
        self.failed_sessions = 0
        self._last_cleanup = None
        self._session_times = []
        
    @property
    def stats(self) -> dict:
        """获取会话统计信息"""
        return {
            "active_sessions": self.active_sessions,
            "total_sessions": self.total_sessions,
            "failed_sessions": self.failed_sessions,
            "avg_session_time": sum(self._session_times) / len(self._session_times) if self._session_times else 0,
            "last_cleanup": self._last_cleanup.isoformat() if self._last_cleanup else None
        }
    
    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """获取数据库会话
        
        Yields:
            数据库会话
        """
        session = AsyncSessionLocal()
        start_time = time.time()
        self.active_sessions += 1
        self.total_sessions += 1
        
        try:
            yield session
            await session.commit()
            session_time = time.time() - start_time
            self._session_times.append(session_time)
            
            # 记录慢会话
            if session_time > 1.0:  # 超过1秒的会话
                logger.warning(f"慢会话: {session_time:.2f}秒")
                
        except SQLAlchemyError as e:
            self.failed_sessions += 1
            logger.error(f"会话错误: {str(e)}")
            await session.rollback()
            raise
            
        except Exception as e:
            self.failed_sessions += 1
            logger.error(f"会话异常: {str(e)}")
            await session.rollback()
            raise
            
        finally:
            self.active_sessions -= 1
            await session.close()
            
            # 限制会话时间记录数量
            if len(self._session_times) > 1000:
                self._session_times = self._session_times[-1000:]

# 创建会话管理器实例
session_manager = SessionManager() 