import yaml
import os
from typing import Optional
from fastapi import HTTPException
from models.config import (
    SystemConfig, 
    MonitorConfig, 
    SymlinkConfig, 
    EmbyConfig, 
    SecurityConfig, 
    PasswordPolicy
)
from utils.path import is_valid_path

CONFIG_PATH = "config/config.yml"
_config_instance: Optional[SystemConfig] = None

def get_config() -> SystemConfig:
    """获取配置实例（单例模式）"""
    global _config_instance
    if _config_instance is None:
        _config_instance = load_config()
    return _config_instance

def load_config() -> SystemConfig:
    """加载配置文件"""
    try:
        if not os.path.exists(CONFIG_PATH):
            config = get_default_config()
            save_config(config)
            return config
            
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config_dict = yaml.safe_load(f)
            return SystemConfig(**config_dict)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"加载配置失败: {str(e)}"
        )

def save_config(config: SystemConfig):
    """保存配置到文件"""
    try:
        # 验证路径
        if not is_valid_path(config.symlink.source_dir):
            raise ValueError("无效的源目录路径")
        if not is_valid_path(config.symlink.target_dir):
            raise ValueError("无效的目标目录路径")
            
        # 验证路径映射
        for local_path, emby_path in config.emby.path_mapping.items():
            if not is_valid_path(local_path) or not is_valid_path(emby_path):
                raise ValueError("无效的路径映射")
        
        # 保存配置
        config_dict = config.model_dump()
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.safe_dump(config_dict, f, allow_unicode=True)
            
        # 更新单例实例
        global _config_instance
        _config_instance = config
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"保存配置失败: {str(e)}"
        )

def reload_config() -> SystemConfig:
    """重新加载配置"""
    global _config_instance
    _config_instance = None
    return get_config()

def get_default_config() -> SystemConfig:
    """获取默认配置"""
    return SystemConfig(
        monitor=MonitorConfig(),
        symlink=SymlinkConfig(
            source_dir="/mnt/media/nastool",
            target_dir="/mnt/nastool-nfo"
        ),
        emby=EmbyConfig(
            host="http://emby:8096"
        ),
        security=SecurityConfig(
            password_policy=PasswordPolicy()
        )
    ) 