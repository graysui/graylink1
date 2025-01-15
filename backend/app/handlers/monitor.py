from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

class MonitorState(BaseModel):
    is_running: bool
    last_check: Optional[str] = None
    total_files: int = 0
    monitored_paths: List[str] = []

@router.get("/monitor/status")
async def get_status():
    return {
        "code": 0,
        "data": {
            "is_running": True,
            "last_check": None,
            "total_files": 0,
            "monitored_paths": []
        }
    }

@router.get("/monitor/logs")
async def get_logs(limit: int = 100):
    return {
        "code": 0,
        "data": {
            "logs": []
        }
    }

@router.post("/monitor/start")
async def start_monitor():
    return {
        "code": 0,
        "data": None
    }

@router.post("/monitor/stop")
async def stop_monitor():
    return {
        "code": 0,
        "data": None
    }

@router.post("/monitor/logs/clear")
async def clear_logs():
    return {
        "code": 0,
        "data": None
    }

@router.get("/monitor/stats")
async def get_stats():
    return {
        "code": 0,
        "data": {
            "total_checks": 0,
            "total_changes": 0,
            "last_check_duration": 0
        }
    } 