import os
from typing import Dict, List, Optional
from loguru import logger
from app.utils.symlink import create_symlink
from app.utils.path import normalize_path, get_relative_path
from app.utils.config import get_config

class SymlinkManager:
    """软链接管理器"""
    
    def __init__(self):
        self.config = get_config()
        self._symlinks: Dict[str, Dict] = {}
        self._load_symlinks()
        
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
                                self._symlinks[file_path] = {
                                    'source': target,
                                    'target': file_path,
                                    'valid': os.path.exists(target)
                                }
        except Exception as e:
            logger.error(f"加载软链接失败: {str(e)}")
            
    def create(self, source: str, target: str) -> bool:
        """创建软链接"""
        try:
            source = normalize_path(source)
            target = normalize_path(target)
            
            result = create_symlink(source, target)
            if result is True or result is None:
                self._symlinks[target] = {
                    'source': source,
                    'target': target,
                    'valid': True
                }
                return True
            return False
        except Exception as e:
            logger.error(f"创建软链接失败: {str(e)}")
            return False
            
    def remove(self, target: str) -> bool:
        """删除软链接"""
        try:
            target = normalize_path(target)
            if target in self._symlinks:
                if os.path.exists(target):
                    os.remove(target)
                del self._symlinks[target]
                return True
            return False
        except Exception as e:
            logger.error(f"删除软链接失败: {str(e)}")
            return False
            
    def verify(self) -> Dict[str, int]:
        """验证所有软链接"""
        try:
            valid = 0
            invalid = 0
            missing = 0
            
            for target, info in self._symlinks.items():
                if not os.path.exists(target):
                    missing += 1
                elif not os.path.exists(info['source']):
                    invalid += 1
                else:
                    valid += 1
                    
            return {
                'total': len(self._symlinks),
                'valid': valid,
                'invalid': invalid,
                'missing': missing
            }
        except Exception as e:
            logger.error(f"验证软链接失败: {str(e)}")
            return {
                'total': 0,
                'valid': 0,
                'invalid': 0,
                'missing': 0
            }
            
    def rebuild(self) -> bool:
        """重建所有软链接"""
        try:
            success = True
            for target, info in self._symlinks.items():
                if not os.path.exists(target) or not os.path.exists(info['source']):
                    if not self.create(info['source'], target):
                        success = False
            return success
        except Exception as e:
            logger.error(f"重建软链接失败: {str(e)}")
            return False
            
    def clear(self) -> bool:
        """清除所有软链接"""
        try:
            for target in list(self._symlinks.keys()):
                self.remove(target)
            return True
        except Exception as e:
            logger.error(f"清除软链接失败: {str(e)}")
            return False
            
    def get_all(self) -> List[Dict]:
        """获取所有软链接信息"""
        return [
            {
                'source': info['source'],
                'target': target,
                'valid': os.path.exists(info['source']) and os.path.exists(target)
            }
            for target, info in self._symlinks.items()
        ] 