from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from app.utils.config import get_config, save_config

router = APIRouter(prefix="/settings", tags=["settings"])

class SystemSettings(BaseModel):
    monitor_paths: List[str] = []
    emby_server: Optional[str] = None
    emby_api_key: Optional[str] = None
    gdrive_client_id: Optional[str] = None
    gdrive_client_secret: Optional[str] = None

@router.get("/")
async def get_settings():
    return {
        "code": 0,
        "data": {
            "monitor_paths": [],
            "emby_server": None,
            "emby_api_key": None,
            "gdrive_client_id": None,
            "gdrive_client_secret": None
        }
    }

@router.post("/")
async def update_settings(settings: SystemSettings):
    return {
        "code": 0,
        "data": None
    }

@router.post("/reset")
async def reset_settings():
    return {
        "code": 0,
        "data": None
    } 