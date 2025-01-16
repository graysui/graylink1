"""GrayLink 应用包

提供应用初始化和启动配置。
"""
from fastapi import FastAPI
from loguru import logger

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
        # 初始化缓存
        await default_cache.initialize()
        logger.info("缓存已初始化")

    @app.on_event("shutdown")
    async def shutdown_event():
        """应用关闭时的清理操作"""
        # 清理缓存
        await default_cache.clear()
        if default_cache._cleanup_task:
            default_cache._cleanup_task.cancel()
        logger.info("缓存已清理")

    return app

# 创建应用实例
app = create_app() 