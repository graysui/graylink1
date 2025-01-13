from fastapi import APIRouter, HTTPException
from models.config import SystemConfig
from utils.config import get_config, save_config, reload_config
from utils.emby import test_emby_connection
from typing import Dict

router = APIRouter()

@router.get("/settings")
async def get_settings() -> SystemConfig:
    """获取系统设置"""
    try:
        return get_config()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/settings")
async def save_settings(settings: SystemConfig):
    """保存系统设置"""
    try:
        save_config(settings)
        return {"message": "配置已保存"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/settings/test-emby")
async def test_emby(params: Dict[str, str]):
    """测试Emby连接"""
    try:
        host = params.get("host")
        api_key = params.get("api_key")
        if not host or not api_key:
            raise HTTPException(status_code=400, detail="缺少必要参数")
            
        await test_emby_connection(host, api_key)
        return {"message": "连接成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/settings/reset")
async def reset_settings():
    """重置系统设置"""
    try:
        config = get_config()
        save_config(config)
        return {"message": "配置已重置"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/settings/reload")
async def reload_settings():
    """重新加载配置"""
    try:
        config = reload_config()
        return {"message": "配置已重新加载"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 