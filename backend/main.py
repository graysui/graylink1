from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

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

@app.get("/")
async def root():
    """健康检查接口"""
    return {"status": "ok", "message": "GrayLink API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 