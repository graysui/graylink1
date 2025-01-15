from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from app.utils.config import get_config
from app.models.config import DriveConfig

router = APIRouter(prefix="/gdrive", tags=["gdrive"])

class DriveActivity(BaseModel):
    time: str
    action: str
    file_name: str
    file_id: str

class ActivityResult(BaseModel):
    activities: List[DriveActivity]
    next_page_token: Optional[str] = None

@router.get("/auth-url")
async def get_auth_url():
    return {
        "code": 0,
        "data": {
            "auth_url": "https://accounts.google.com/o/oauth2/auth"
        }
    }

@router.post("/start-auth")
async def start_auth():
    return {
        "code": 0,
        "data": {
            "user_code": "ABCD-EFGH",
            "verification_url": "https://www.google.com/device",
            "device_code": "device_code",
            "expires_in": 1800
        }
    }

@router.post("/check-auth")
async def check_auth(device_code: str):
    return {
        "code": 0,
        "data": {
            "status": "pending"
        }
    }

@router.get("/check-activities")
async def check_activities():
    return {
        "code": 0,
        "data": {
            "activities": [],
            "next_page_token": None
        }
    }

@router.get("/test")
async def test_connection():
    return {
        "code": 0,
        "data": None
    } 