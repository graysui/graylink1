from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from app.utils.symlink import create_symlink

router = APIRouter(prefix="/symlink", tags=["symlink"])

class SymlinkState(BaseModel):
    total: int
    valid: int
    invalid: int

@router.get("/verify")
async def verify_symlinks():
    return {
        "code": 0,
        "data": {
            "total": 0,
            "valid": 0,
            "invalid": 0
        }
    }

@router.post("/")
async def create_symlink(data: dict):
    return {
        "code": 0,
        "data": None
    }

@router.delete("/{id}")
async def remove_symlink(id: str):
    return {
        "code": 0,
        "data": None
    }

@router.delete("/")
async def clear_symlinks():
    return {
        "code": 0,
        "data": None
    }

@router.post("/rebuild")
async def rebuild_symlinks():
    return {
        "code": 0,
        "data": None
    } 