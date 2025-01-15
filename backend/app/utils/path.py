import os
from typing import List

def normalize_path(path: str) -> str:
    """
    规范化路径，统一使用正斜杠
    """
    return path.replace('\\', '/')

def get_relative_path(base_path: str, full_path: str) -> str:
    """
    获取相对路径
    """
    base_path = normalize_path(base_path)
    full_path = normalize_path(full_path)
    
    if not full_path.startswith(base_path):
        raise ValueError("full_path必须以base_path开头")
        
    rel_path = full_path[len(base_path):].lstrip('/')
    return rel_path

def list_files(directory: str, recursive: bool = True) -> List[str]:
    """
    列出目录下的所有文件
    """
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append(normalize_path(file_path))
        if not recursive:
            break
    return files 