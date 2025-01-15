import os
import json
from typing import Optional
from pydantic import BaseModel

class DriveConfig(BaseModel):
    enabled: bool = False
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    token_file: Optional[str] = None

class EmbyConfig(BaseModel):
    enabled: bool = False
    server: Optional[str] = None
    api_key: Optional[str] = None

class MonitorConfig(BaseModel):
    interval: int = 60000  # 默认60秒
    google_drive: DriveConfig = DriveConfig()

class Config(BaseModel):
    monitor: MonitorConfig = MonitorConfig()
    emby: EmbyConfig = EmbyConfig()

_config: Optional[Config] = None

def load_config(config_file: str = "config/config.json") -> Config:
    """加载配置文件"""
    global _config
    
    if _config:
        return _config
        
    if not os.path.exists(config_file):
        # 创建默认配置
        _config = Config()
        save_config(_config, config_file)
        return _config
        
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            _config = Config(**config_data)
            return _config
    except Exception as e:
        # 如果配置文件损坏，创建默认配置
        _config = Config()
        save_config(_config, config_file)
        return _config

def save_config(config: Config, config_file: str = "config/config.json"):
    """保存配置文件"""
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config.dict(), f, ensure_ascii=False, indent=2)

def get_config() -> Config:
    """获取配置实例"""
    global _config
    if not _config:
        _config = load_config()
    return _config 