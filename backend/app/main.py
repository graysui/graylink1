from fastapi import FastAPI
from handlers import setting, file, gdrive, emby, symlink, monitor
from fastapi.middleware.cors import CORSMiddleware
from middleware.config import config_middleware
import logging
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时的操作
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