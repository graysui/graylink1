from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as e:
        logger.warning(f"HTTP异常: {str(e)}")
        return JSONResponse(
            status_code=e.status_code,
            content={"error": str(e.detail)}
        )
    except Exception as e:
        logger.error(f"未处理异常: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": "服务器内部错误"}
        ) 