"""数据库管理模块

提供数据库连接和会话管理。
"""
import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool

from app.core.config import settings

# 配置日志
logger = logging.getLogger(__name__)

# 创建异步引擎
engine = create_async_engine(
    settings.database.url,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    pool_timeout=settings.database.pool_timeout,
    pool_recycle=settings.database.pool_recycle,
    echo=settings.database.echo,
    poolclass=AsyncAdaptedQueuePool
)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话
    
    Yields:
        数据库会话
    """
    session = AsyncSessionLocal()
    try:
        yield session
    except Exception as e:
        logger.error(f"数据库会话异常: {str(e)}")
        await session.rollback()
        raise
    finally:
        await session.close()

async def init_db() -> None:
    """
    初始化数据库
    创建所有表和初始数据
    """
    from .base import Base  # 避免循环导入
    
    async with engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)
        
    logger.info("数据库初始化完成")

async def get_db_stats() -> dict:
    """
    获取数据库统计信息
    包括连接池状态
    """
    return {
        "pool_stats": {
            "size": engine.pool.size(),
            "checked_in": engine.pool.checkedin(),
            "checked_out": engine.pool.checkedout(),
            "overflow": engine.pool.overflow()
        }
    } 