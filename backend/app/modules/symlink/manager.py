import os
import shutil
from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger
from pathlib import Path
from ...core.config import settings

class SymlinkManager:
    def __init__(self):
        self.source_dir = settings.symlink.source_dir  # rclone挂载路径，如 /mnt/media/nastool
        self.target_dir = settings.symlink.target_dir  # 软链接目标路径，如 /mnt/nastool-nfo
        self._ensure_directories()

    def _ensure_directories(self):
        """确保必要的目录存在"""
        os.makedirs(self.source_dir, exist_ok=True)
        os.makedirs(self.target_dir, exist_ok=True)

    async def create_symlink(self, relative_path: str) -> bool:
        """创建软链接
        
        Args:
            relative_path: 相对路径，如 "剧集/国产剧/一二/1.mkv"
        """
        try:
            # 构建完整的源文件路径和目标路径
            source_path = os.path.join(self.source_dir, relative_path)
            target_path = os.path.join(self.target_dir, relative_path)
            target_dir = os.path.dirname(target_path)

            # 检查源文件是否存在
            if not os.path.exists(source_path):
                logger.error(f"Source file does not exist: {source_path}")
                return False

            # 创建目标目录结构
            os.makedirs(target_dir, exist_ok=True)

            # 检查目标路径是否已存在
            if os.path.exists(target_path):
                if os.path.islink(target_path):
                    current_source = os.path.realpath(target_path)
                    if current_source == source_path:
                        return True  # 已经存在相同的软链接
                    os.unlink(target_path)  # 删除现有的软链接
                else:
                    # 如果是实体文件或目录，重命名为备份
                    backup_path = f"{target_path}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    shutil.move(target_path, backup_path)
                    logger.warning(f"Existing file backed up: {target_path} -> {backup_path}")

            # 创建软链接，保持相对路径结构
            os.symlink(source_path, target_path)
            logger.info(f"Created symlink: {target_path} -> {source_path}")
            return True

        except Exception as e:
            logger.error(f"Error creating symlink for {relative_path}: {str(e)}")
            return False

    async def remove_symlink(self, relative_path: str) -> bool:
        """删除软链接"""
        try:
            target_path = os.path.join(self.target_dir, relative_path)
            
            if os.path.islink(target_path):
                os.unlink(target_path)
                logger.info(f"Removed symlink: {target_path}")
                
                # 清理空目录
                await self._cleanup_empty_dirs(os.path.dirname(target_path))
                return True
            return False

        except Exception as e:
            logger.error(f"Error removing symlink {target_path}: {str(e)}")
            return False

    async def _cleanup_empty_dirs(self, path: str):
        """清理空目录"""
        try:
            current = Path(path)
            while current != Path(self.target_dir):
                if not any(current.iterdir()):
                    current.rmdir()
                    logger.info(f"Removed empty directory: {current}")
                    current = current.parent
                else:
                    break
        except Exception as e:
            logger.error(f"Error cleaning up directories: {str(e)}")

    async def verify_symlinks(self) -> Dict[str, int]:
        """验证所有软链接的完整性"""
        valid_count = 0
        invalid_count = 0
        missing_count = 0
        
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                full_path = os.path.join(root, file)
                if os.path.islink(full_path):
                    target = os.path.realpath(full_path)
                    if not os.path.exists(target):
                        missing_count += 1
                    elif not target.startswith(self.source_dir):
                        invalid_count += 1
                    else:
                        valid_count += 1

        return {
            "valid": valid_count,
            "invalid": invalid_count,
            "missing": missing_count
        }

    async def rebuild_symlinks(self, file_records: List[Dict]) -> Dict[str, int]:
        """重建所有软链接"""
        try:
            # 清理现有的软链接
            await self.clear_all_symlinks()
            
            valid_count = 0
            invalid_count = 0
            missing_count = 0
            
            for record in file_records:
                source_path = os.path.join(self.source_dir, record['path'])
                if not os.path.exists(source_path):
                    missing_count += 1
                    continue
                    
                if await self.create_symlink(record['path']):
                    valid_count += 1
                else:
                    invalid_count += 1

            return {
                "valid": valid_count,
                "invalid": invalid_count,
                "missing": missing_count
            }

        except Exception as e:
            logger.error(f"Error rebuilding symlinks: {str(e)}")
            raise

    async def clear_all_symlinks(self) -> int:
        """清理所有软链接"""
        removed_count = 0
        
        for root, _, files in os.walk(self.target_dir, topdown=False):
            for file in files:
                full_path = os.path.join(root, file)
                if os.path.islink(full_path):
                    try:
                        os.unlink(full_path)
                        removed_count += 1
                    except Exception as e:
                        logger.error(f"Error removing symlink {full_path}: {str(e)}")

            # 尝试删除空目录
            if root != self.target_dir:
                try:
                    os.rmdir(root)
                except OSError:
                    pass  # 目录不为空，跳过

        return removed_count 