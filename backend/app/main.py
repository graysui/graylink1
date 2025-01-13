from fastapi import FastAPI
from handlers import setting, file
from fastapi.middleware.cors import CORSMiddleware
from middleware.config import config_middleware
import logging
from fastapi.responses import JSONResponse

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加配置中间件
app.middleware("http")(config_middleware)

# 注册路由
app.include_router(setting.router, prefix="/api", tags=["settings"])
app.include_router(file.router, prefix="/api", tags=["files"])

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global error handler: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    ) 