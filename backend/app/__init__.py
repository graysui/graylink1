"""GrayLink 应用包

提供应用初始化和启动配置。
"""
from fastapi import FastAPI
from loguru import logger
import asyncio

from app.core.config import settings
from app.core.cache import cleanup_cache, default_cache

def create_app() -> FastAPI:
    """创建并配置 FastAPI 应用实例"""
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug
    )

    @app.on_event("startup")
    async def startup_event():
        """应用启动时的初始化操作"""
        # 启动缓存清理任务
        asyncio.create_task(
            cleanup_cache(interval=settings.cache.cleanup_interval)
        )
        logger.info("缓存清理任务已启动")

    @app.on_event("shutdown")
    async def shutdown_event():
        """应用关闭时的清理操作"""
        # 清理缓存
        default_cache.clear()
        logger.info("缓存已清理")

    return app

# 创建应用实例
app = create_app() 