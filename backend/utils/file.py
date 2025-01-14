import os
import shutil
from datetime import datetime
from typing import Dict, List
from schemas.file import FileOperation

def get_file_info(path: str) -> Dict:
    """获取文件信息"""
    stat = os.stat(path)
    name = os.path.basename(path)
    _, ext = os.path.splitext(name)
    
    return {
        "name": name,
        "path": path,
        "type": "directory" if os.path.isdir(path) else "file",
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "extension": ext[1:] if ext else None
    }

async def batch_operation(operation: FileOperation, paths: List[str], target_path: str = None) -> Dict:
    """批量文件操作"""
    success = []
    failed = []
    
    try:
        for path in paths:
            try:
                if operation == FileOperation.DELETE:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                elif operation == FileOperation.COPY and target_path:
                    if os.path.isdir(path):
                        shutil.copytree(path, os.path.join(target_path, os.path.basename(path)))
                    else:
                        shutil.copy2(path, target_path)
                elif operation == FileOperation.MOVE and target_path:
                    shutil.move(path, target_path)
                success.append(path)
            except Exception as e:
                failed.append({"path": path, "error": str(e)})
                
        return {
            "success": success,
            "failed": failed
        }
    except Exception as e:
        raise Exception(f"批量操作失败: {str(e)}") 