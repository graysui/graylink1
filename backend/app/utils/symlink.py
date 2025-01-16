"""软链接工具模块

提供软链接操作的底层工具函数。
"""
import os
import stat
import shutil
from pathlib import Path
from typing import Optional, Tuple, List
from loguru import logger

def create_symlink(source_path: str, target_path: str, force: bool = False) -> Optional[bool]:
    """创建软链接
    
    Args:
        source_path: 源文件路径
        target_path: 目标软链接路径
        force: 是否强制创建（忽略权限检查）
        
    Returns:
        bool: 创建成功返回True，失败返回False
        None: 如果目标已存在且是正确的软链接
        
    Raises:
        OSError: 如果没有足够的权限
        FileNotFoundError: 如果源文件不存在
    """
    try:
        source_path = os.path.abspath(source_path)
        target_path = os.path.abspath(target_path)
        
        # 检查源文件
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"源文件不存在: {source_path}")
            
        # 检查目标路径
        if os.path.exists(target_path):
            if os.path.islink(target_path):
                current_target = os.path.realpath(target_path)
                if current_target == source_path:
                    logger.debug(f"软链接已存在且正确: {target_path} -> {source_path}")
                    return None
                    
            # 如果存在但不是正确的软链接，尝试删除
            try:
                os.remove(target_path)
            except PermissionError as e:
                if not force:
                    raise OSError(f"没有权限删除已存在的目标文件: {target_path}")
                # 强制删除
                os.chmod(target_path, stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
                os.remove(target_path)
                
        # 创建目标文件夹
        target_dir = os.path.dirname(target_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
            
        # 创建软链接
        os.symlink(source_path, target_path)
        logger.info(f"成功创建软链接: {target_path} -> {source_path}")
        return True
        
    except Exception as e:
        logger.error(f"创建软链接失败: {source_path} -> {target_path}, 错误: {str(e)}")
        return False

def verify_symlink(path: str) -> Tuple[bool, Optional[str]]:
    """验证软链接
    
    Args:
        path: 软链接路径
        
    Returns:
        (bool, str): (是否有效, 错误信息)
    """
    try:
        if not os.path.exists(path):
            return False, "链接不存在"
            
        if not os.path.islink(path):
            return False, "不是软链接"
            
        target = os.path.realpath(path)
        if not os.path.exists(target):
            return False, "目标文件不存在"
            
        return True, None
        
    except Exception as e:
        return False, str(e)

def find_broken_symlinks(directory: str) -> List[str]:
    """查找目录中的无效软链接
    
    Args:
        directory: 要搜索的目录
        
    Returns:
        无效软链接的路径列表
    """
    broken_links = []
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                path = os.path.join(root, file)
                if os.path.islink(path):
                    is_valid, _ = verify_symlink(path)
                    if not is_valid:
                        broken_links.append(path)
        return broken_links
    except Exception as e:
        logger.error(f"查找无效软链接失败: {str(e)}")
        return []

def repair_symlink(path: str, source_path: Optional[str] = None) -> bool:
    """修复软链接
    
    Args:
        path: 软链接路径
        source_path: 可选的新源文件路径
        
    Returns:
        是否修复成功
    """
    try:
        if not os.path.islink(path):
            return False
            
        # 如果没有提供新的源路径，尝试使用原始目标
        if not source_path:
            source_path = os.path.realpath(path)
            
        # 如果源文件不存在，无法修复
        if not os.path.exists(source_path):
            return False
            
        # 删除原有链接
        os.remove(path)
        
        # 创建新链接
        return create_symlink(source_path, path) is True
        
    except Exception as e:
        logger.error(f"修复软链接失败 [{path}]: {str(e)}")
        return False

def copy_with_symlinks(src: str, dst: str, follow_symlinks: bool = True) -> bool:
    """复制文件或目录，保持软链接
    
    Args:
        src: 源路径
        dst: 目标路径
        follow_symlinks: 是否跟随软链接
        
    Returns:
        是否复制成功
    """
    try:
        if os.path.islink(src) and not follow_symlinks:
            # 复制软链接本身
            linkto = os.readlink(src)
            os.symlink(linkto, dst)
            return True
            
        elif os.path.isdir(src):
            # 复制目录
            if not os.path.exists(dst):
                os.makedirs(dst)
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                copy_with_symlinks(s, d, follow_symlinks)
            return True
            
        else:
            # 复制文件
            shutil.copy2(src, dst)
            return True
            
    except Exception as e:
        logger.error(f"复制失败 [{src} -> {dst}]: {str(e)}")
        return False 