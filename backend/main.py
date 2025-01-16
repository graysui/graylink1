from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import os

# 导入数据库相关
from app.core.base import Base as BaseModel
from app.core.database import engine, get_db
from app.core.config import settings
from app.models.user import Base

# 导入处理器
from app.handlers import auth, monitor, file, symlink, emby, gdrive

# 创建必要的目录
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)

# 创建FastAPI应用
app = FastAPI(
    title="GrayLink API",
    description="GrayLink backend API service",
    version="0.1.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中需要修改为具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置日志
logger.add(
    "logs/graylink.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO" if not settings.debug else "DEBUG"
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(monitor.router, prefix="/api/monitor", tags=["监控"])
app.include_router(file.router, prefix="/api/file", tags=["文件"])
app.include_router(symlink.router, prefix="/api/symlink", tags=["软链接"])
app.include_router(emby.router, prefix="/api/emby", tags=["Emby"])
app.include_router(gdrive.router, prefix="/api/gdrive", tags=["Google Drive"])

@app.get("/")
async def root():
    """健康检查接口"""
    return {
        "status": "ok",
        "message": "GrayLink API is running",
        "version": "0.1.0"
    }

@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化操作"""
    logger.info("正在初始化应用...")
    
    # 创建数据库表
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("数据库表创建成功")
    except Exception as e:
        logger.error(f"数据库表创建失败: {str(e)}")
        raise
    
    # 初始化默认用户
    try:
        async for db in get_db():
            await auth.init_default_user(db)
            logger.info("默认用户初始化成功")
            break
    except Exception as e:
        logger.error(f"默认用户初始化失败: {str(e)}")
        raise

    logger.info("应用初始化完成")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    ) 