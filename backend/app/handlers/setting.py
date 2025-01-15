from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

class SystemSettings(BaseModel):
    monitor_paths: List[str] = []
    emby_server: Optional[str] = None
    emby_api_key: Optional[str] = None
    gdrive_client_id: Optional[str] = None
    gdrive_client_secret: Optional[str] = None

@router.get("/settings")
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

@router.post("/settings")
async def update_settings(settings: SystemSettings):
    return {
        "code": 0,
        "data": None
    }

@router.post("/settings/reset")
async def reset_settings():
    return {
        "code": 0,
        "data": None
    } 