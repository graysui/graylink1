"""GrayLink 后端服务

提供 GrayLink 的后端 API 服务。
"""
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.base import Base as BaseModel
from app.core.database import engine, AsyncSessionLocal
from app.core.cache import default_cache
from app.core.session import SessionManager, session_manager
from app.core.auth import AuthManager
from app.handlers import auth, monitor, file, symlink, emby, gdrive
from app.core.config import settings

# 初始化会话管理器
session_manager.init_session_factory(AsyncSessionLocal)

# 创建应用实例
app = FastAPI(
    title="GrayLink API",
    description="GrayLink 后端 API 服务",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api", tags=["认证"])
app.include_router(monitor.router, prefix="/api/monitor", tags=["监控"])
app.include_router(file.router, prefix="/api/file", tags=["文件"])
app.include_router(symlink.router, prefix="/api/symlink", tags=["符号链接"])
app.include_router(emby.router, prefix="/api/emby", tags=["Emby"])
app.include_router(gdrive.router, prefix="/api/gdrive", tags=["Google Drive"])

@app.on_event("startup")
async def startup():
    """应用启动时的初始化操作"""
    try:
        # 确保数据目录存在
        settings.ensure_data_directory()
        
        # 创建数据库表
        async with engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)
            
        # 初始化缓存
        await default_cache.initialize()
        
        # 初始化会话管理器
        session_manager = SessionManager.get_instance()
        
        # 初始化认证管理器
        auth_manager = AuthManager.get_instance()
            
        logger.info("应用初始化完成")
        
    except Exception as e:
        logger.error(f"应用初始化失败: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown():
    """应用关闭时的清理操作"""
    try:
        # 关闭数据库连接
        await engine.dispose()
        
        # 清理缓存
        await default_cache.clear()
        if default_cache._cleanup_task:
            default_cache._cleanup_task.cancel()
            
        logger.info("应用清理完成")
        
    except Exception as e:
        logger.error(f"应用清理失败: {str(e)}")
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 