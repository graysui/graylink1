import os
import shutil
from datetime import datetime
from typing import Dict, List, Optional

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

def list_directory(path: str) -> List[Dict]:
    """列出目录内容"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"路径不存在: {path}")
        
    if not os.path.isdir(path):
        raise NotADirectoryError(f"不是目录: {path}")
        
    items = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        items.append(get_file_info(item_path))
        
    return items

def batch_operation(operation: str, paths: List[str], target_path: Optional[str] = None) -> Dict[str, List[str]]:
    """批量文件操作"""
    success = []
    failed = []
    
    try:
        for path in paths:
            try:
                if operation == "DELETE":
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                elif operation == "MOVE" and target_path:
                    shutil.move(path, target_path)
                elif operation == "COPY" and target_path:
                    if os.path.isdir(path):
                        shutil.copytree(path, target_path)
                    else:
                        shutil.copy2(path, target_path)
                success.append(path)
            except Exception as e:
                failed.append(path)
                
    except Exception as e:
        # 处理整体操作失败的情况
        pass
        
    return {
        "success": success,
        "failed": failed
    } 