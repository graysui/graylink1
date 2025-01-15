from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from handlers import auth, monitor, file, symlink, emby, gdrive
from models.user import Base
from app.core.database import engine, get_db

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
    level="INFO"
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
    return {"status": "ok", "message": "GrayLink API is running"}

@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化操作"""
    # 创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 初始化默认用户
    async for db in get_db():
        await auth.init_default_user(db)
        break

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 