from fastapi import APIRouter, HTTPException
from typing import List
import os
from models.file import FileInfo

router = APIRouter()

@router.get("/file/list")
async def list_directory(path: str) -> List[FileInfo]:
    """获取目录列表"""
    try:
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="路径不存在")
            
        if not os.path.isdir(path):
            raise HTTPException(status_code=400, detail="不是有效的目录")
            
        items = []
        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            items.append(FileInfo(
                name=name,
                path=full_path,
                is_directory=os.path.isdir(full_path)
            ))
            
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 