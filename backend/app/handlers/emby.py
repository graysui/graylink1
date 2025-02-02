from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from app.utils.emby import EmbyClient
from app.utils.config import get_config

router = APIRouter(tags=["emby"])

class EmbyStatus(BaseModel):
    connected: bool
    version: Optional[str] = None
    server_name: Optional[str] = None

class EmbyLibrary(BaseModel):
    id: str
    name: str
    path: str

@router.get("/status")
async def check_status():
    return {
        "code": 0,
        "data": {
            "connected": True,
            "version": "4.7.0.0",
            "server_name": "Emby Server"
        }
    }

@router.get("/libraries")
async def get_libraries():
    return {
        "code": 0,
        "data": []
    }

@router.post("/refresh")
async def refresh_by_paths(paths: List[str]):
    return {
        "code": 0,
        "data": None
    }

@router.post("/refresh/root")
async def refresh_root():
    return {
        "code": 0,
        "data": None
    }

@router.post("/test")
async def test_connection():
    return {
        "code": 0,
        "data": None
    } 