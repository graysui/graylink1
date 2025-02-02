from fastapi import FastAPI
from handlers import setting, file, gdrive, emby, symlink, monitor, auth
from fastapi.middleware.cors import CORSMiddleware
from middleware.config import config_middleware
import logging
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.core.database import engine, Base
from app.models.user import User
from app.handlers.auth import init_default_user
from sqlalchemy.ext.asyncio import AsyncSession
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时的操作
    
    # 确保data目录存在
    os.makedirs("data", exist_ok=True)
    
    # 创建所有表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 初始化默认用户
    async with AsyncSession(engine) as db:
        await init_default_user(db)
    
    yield
    # 关闭时的操作

app = FastAPI(lifespan=lifespan)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加配置中间件
app.middleware("http")(config_middleware)

# 注册路由
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(setting.router, prefix="/api", tags=["settings"])
app.include_router(file.router, prefix="/api", tags=["files"])
app.include_router(gdrive.router, prefix="/api", tags=["gdrive"])
app.include_router(emby.router, prefix="/api", tags=["emby"])
app.include_router(symlink.router, prefix="/api", tags=["symlink"])
app.include_router(monitor.router, prefix="/api", tags=["monitor"])

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global error handler: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    ) 