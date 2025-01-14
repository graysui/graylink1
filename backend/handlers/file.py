from fastapi import APIRouter, HTTPException
from typing import List, Dict
import os
from models.file import FileInfo
from schemas.file import BatchOperationRequest
from utils.file import get_file_info, batch_operation

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

@router.get("/monitor/snapshot")
async def get_snapshot(path: str) -> Dict:
    """获取文件快照"""
    try:
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="路径不存在")
        
        items = []
        total_size = 0
        
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for name in files:
                    file_path = os.path.join(root, name)
                    file_info = get_file_info(file_path)
                    items.append(file_info)
                    total_size += file_info.get('size', 0)
        else:
            file_info = get_file_info(path)
            items.append(file_info)
            total_size = file_info.get('size', 0)
            
        return {
            "code": 200,
            "data": {
                "items": items,
                "total": len(items),
                "size": total_size,
                "path": path
            },
            "message": "获取快照成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/file/batch")
async def batch_file_operation(request: BatchOperationRequest) -> Dict:
    """批量文件操作"""
    try:
        result = await batch_operation(
            operation=request.operation,
            paths=request.paths,
            target_path=request.target_path
        )
        return {
            "code": 200,
            "data": result,
            "message": "操作成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 