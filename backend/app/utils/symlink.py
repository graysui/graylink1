import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def create_symlink(source_path: str, target_path: str) -> Optional[bool]:
    """
    创建软链接
    
    Args:
        source_path: 源文件路径
        target_path: 目标软链接路径
        
    Returns:
        bool: 创建成功返回True，失败返回False
        None: 如果目标已存在且是正确的软链接
    """
    try:
        # 确保源文件存在
        if not os.path.exists(source_path):
            logger.error(f"源文件不存在: {source_path}")
            return False
            
        # 如果目标已存在
        if os.path.exists(target_path):
            # 如果是软链接且指向正确的源文件
            if os.path.islink(target_path) and os.path.realpath(target_path) == os.path.realpath(source_path):
                logger.debug(f"软链接已存在且正确: {target_path} -> {source_path}")
                return None
            # 如果存在但不是正确的软链接，删除它
            try:
                os.remove(target_path)
            except Exception as e:
                logger.error(f"删除已存在的目标文件失败: {target_path}, 错误: {str(e)}")
                return False
        
        # 创建目标文件夹（如果不存在）
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