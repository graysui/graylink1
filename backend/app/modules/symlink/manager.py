"""软链接管理模块

提供软链接的创建、管理和监控功能。
"""
import os
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Set
from pathlib import Path
from loguru import logger
from app.utils.symlink import create_symlink
from app.utils.path import normalize_path, get_relative_path
from app.utils.config import get_config
from app.core.cache import cached

class SymlinkError(Exception):
    """软链接操作异常"""
    pass

class SymlinkManager:
    """软链接管理器
    
    管理文件系统软链接的创建、删除和维护。
    """
    
    def __init__(self, backup_dir: Optional[str] = None):
        """初始化软链接管理器
        
        Args:
            backup_dir: 备份目录路径，默认为 'data/symlink_backups'
        """
        self.config = get_config()
        self._symlinks: Dict[str, Dict] = {}
        self._backup_dir = backup_dir or 'data/symlink_backups'
        self._stats = {
            'created': 0,
            'removed': 0,
            'failed': 0,
            'last_operation': None,
            'last_error': None
        }
        
        # 确保备份目录存在
        os.makedirs(self._backup_dir, exist_ok=True)
        self._load_symlinks()
        
    @property
    def stats(self) -> Dict:
        """获取管理器统计信息"""
        verify_result = self.verify()
        return {
            **self._stats,
            **verify_result,
            'backup_size': self._get_backup_size(),
            'last_operation_time': self._stats['last_operation'].isoformat() if self._stats['last_operation'] else None
        }
        
    def _load_symlinks(self):
        """加载已存在的软链接"""
        try:
            # 从配置的监控路径中加载软链接
            for path in self.config.monitor.paths:
                if os.path.exists(path):
                    for root, _, files in os.walk(path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            if os.path.islink(file_path):
                                target = os.path.realpath(file_path)
                                self._add_symlink(target, file_path)
        except Exception as e:
            logger.error(f"加载软链接失败: {str(e)}")
            self._update_stats(failed=True, error=e)
            
    def _add_symlink(self, source: str, target: str):
        """添加软链接记录"""
        self._symlinks[target] = {
            'source': source,
            'target': target,
            'valid': os.path.exists(source),
            'created_at': datetime.now(),
            'last_checked': datetime.now()
        }
        
    def _update_stats(self, created: bool = False, removed: bool = False, failed: bool = False, error: Optional[Exception] = None):
        """更新统计信息"""
        if created:
            self._stats['created'] += 1
        if removed:
            self._stats['removed'] += 1
        if failed:
            self._stats['failed'] += 1
        if error:
            self._stats['last_error'] = str(error)
        self._stats['last_operation'] = datetime.now()
            
    def create(self, source: str, target: str, backup: bool = True) -> bool:
        """创建软链接
        
        Args:
            source: 源文件路径
            target: 目标路径
            backup: 是否备份已存在的文件
            
        Returns:
            是否创建成功
        """
        try:
            source = normalize_path(source)
            target = normalize_path(target)
            
            # 检查源文件是否存在
            if not os.path.exists(source):
                raise SymlinkError(f"源文件不存在: {source}")
            
            # 如果目标已存在且不是软链接，进行备份
            if os.path.exists(target) and not os.path.islink(target):
                if backup:
                    self._backup_file(target)
                os.remove(target)
            
            result = create_symlink(source, target)
            if result is True or result is None:
                self._add_symlink(source, target)
                self._update_stats(created=True)
                logger.info(f"创建软链接成功: {target} -> {source}")
                return True
                
            self._update_stats(failed=True)
            return False
            
        except Exception as e:
            logger.error(f"创建软链接失败: {str(e)}")
            self._update_stats(failed=True, error=e)
            return False
            
    def remove(self, target: str, cleanup: bool = True) -> bool:
        """删除软链接
        
        Args:
            target: 目标路径
            cleanup: 是否清理相关记录
            
        Returns:
            是否删除成功
        """
        try:
            target = normalize_path(target)
            if target in self._symlinks:
                if os.path.exists(target):
                    if not os.path.islink(target):
                        raise SymlinkError(f"目标不是软链接: {target}")
                    os.remove(target)
                if cleanup:
                    del self._symlinks[target]
                self._update_stats(removed=True)
                logger.info(f"删除软链接成功: {target}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"删除软链接失败: {str(e)}")
            self._update_stats(failed=True, error=e)
            return False
            
    @cached(prefix="symlink_manager", ttl=300)
    def verify(self) -> Dict[str, int]:
        """验证所有软链接
        
        Returns:
            验证结果统计
        """
        try:
            valid = 0
            invalid = 0
            missing = 0
            orphaned = set()
            
            # 检查记录的软链接
            for target, info in self._symlinks.items():
                if not os.path.exists(target):
                    missing += 1
                elif not os.path.exists(info['source']):
                    invalid += 1
                    orphaned.add(target)
                else:
                    valid += 1
                    info['last_checked'] = datetime.now()
                    
            # 自动清理无效的软链接
            for target in orphaned:
                self.remove(target)
                    
            return {
                'total': len(self._symlinks),
                'valid': valid,
                'invalid': invalid,
                'missing': missing,
                'orphaned': len(orphaned)
            }
            
        except Exception as e:
            logger.error(f"验证软链接失败: {str(e)}")
            self._update_stats(failed=True, error=e)
            return {
                'total': 0,
                'valid': 0,
                'invalid': 0,
                'missing': 0,
                'orphaned': 0
            }
            
    async def rebuild(self, verify_first: bool = True) -> bool:
        """重建所有软链接
        
        Args:
            verify_first: 是否先进行验证
            
        Returns:
            是否重建成功
        """
        try:
            if verify_first:
                self.verify()
                
            success = True
            for target, info in self._symlinks.items():
                if not os.path.exists(target) or not os.path.exists(info['source']):
                    if not self.create(info['source'], target):
                        success = False
                        
            return success
            
        except Exception as e:
            logger.error(f"重建软链接失败: {str(e)}")
            self._update_stats(failed=True, error=e)
            return False
            
    def clear(self, backup: bool = True) -> bool:
        """清除所有软链接
        
        Args:
            backup: 是否备份文件
            
        Returns:
            是否清除成功
        """
        try:
            for target in list(self._symlinks.keys()):
                if backup and os.path.exists(target):
                    self._backup_file(target)
                self.remove(target)
            return True
            
        except Exception as e:
            logger.error(f"清除软链接失败: {str(e)}")
            self._update_stats(failed=True, error=e)
            return False
            
    def get_all(self) -> List[Dict]:
        """获取所有软链接信息"""
        return [
            {
                'source': info['source'],
                'target': target,
                'valid': os.path.exists(info['source']) and os.path.exists(target),
                'created_at': info['created_at'].isoformat(),
                'last_checked': info['last_checked'].isoformat()
            }
            for target, info in self._symlinks.items()
        ]
        
    def _backup_file(self, file_path: str):
        """备份文件
        
        Args:
            file_path: 要备份的文件路径
        """
        try:
            if not os.path.exists(file_path):
                return
                
            # 创建备份文件名
            backup_name = f"{Path(file_path).name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_path = os.path.join(self._backup_dir, backup_name)
            
            # 复制文件到备份目录
            shutil.copy2(file_path, backup_path)
            logger.info(f"文件已备份: {backup_path}")
            
        except Exception as e:
            logger.error(f"备份文件失败 [{file_path}]: {str(e)}")
            raise
            
    def _get_backup_size(self) -> int:
        """获取备份目录大小（字节）"""
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(self._backup_dir):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
            return total_size
        except Exception as e:
            logger.error(f"获取备份大小失败: {str(e)}")
            return 0
            
    def cleanup_backups(self, max_age_days: int = 30) -> int:
        """清理过期的备份文件
        
        Args:
            max_age_days: 最大保留天数
            
        Returns:
            清理的文件数量
        """
        try:
            cleaned = 0
            cutoff_time = datetime.now().timestamp() - (max_age_days * 86400)
            
            for f in os.listdir(self._backup_dir):
                file_path = os.path.join(self._backup_dir, f)
                if os.path.getctime(file_path) < cutoff_time:
                    os.remove(file_path)
                    cleaned += 1
                    
            logger.info(f"清理了 {cleaned} 个过期备份文件")
            return cleaned
            
        except Exception as e:
            logger.error(f"清理备份失败: {str(e)}")
            return 0 