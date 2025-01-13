from fastapi import Request
from utils.config import get_config

async def config_middleware(request: Request, call_next):
    """配置中间件，确保配置已加载"""
    try:
        # 确保配置已加载
        get_config()
        response = await call_next(request)
        return response
    except Exception as e:
        return {
            "status_code": 500,
            "detail": f"配置加载失败: {str(e)}"
        } 