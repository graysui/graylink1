import os
from typing import List

def normalize_path(path: str) -> str:
    """规范化路径"""
    return os.path.normpath(path)

def is_valid_path(path: str) -> bool:
    """验证路径是否有效"""
    try:
        normalized = normalize_path(path)
        return (
            normalized.startswith('/') and
            '..' not in normalized.split('/') and
            not any(c in normalized for c in ['<', '>', '|', '*', '?'])
        )
    except:
        return False

def list_directories(path: str) -> List[str]:
    """列出目录下的所有子目录"""
    try:
        if not os.path.exists(path):
            return []
            
        return [
            d for d in os.listdir(path)
            if os.path.isdir(os.path.join(path, d))
        ]
    except:
        return [] 