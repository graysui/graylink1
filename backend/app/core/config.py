from pydantic_settings import BaseSettings
from pydantic import BaseModel
from typing import Optional, Dict
import yaml
import os

class GoogleDriveSettings(BaseModel):
    client_id: str = ""
    client_secret: str = ""
    token_file: str = "data/gdrive_token.json"

class MonitorSettings(BaseModel):
    scan_interval: int = 300
    google_drive: GoogleDriveSettings = GoogleDriveSettings()

class SymlinkSettings(BaseModel):
    source_dir: str = "/mnt/media/nastool"
    target_dir: str = "/mnt/nastool-nfo"
    preserve_structure: bool = True
    backup_on_conflict: bool = True

class EmbySettings(BaseModel):
    host: str = "http://emby:8096"
    api_key: str = ""
    auto_refresh: bool = True
    refresh_delay: int = 10
    path_mapping: Dict[str, str] = {}

class DatabaseSettings(BaseModel):
    url: str = "sqlite+aiosqlite:///data/graylink.db"
    pool_size: int = 20
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 3600
    echo: bool = False
    batch_size: int = 1000

class Settings(BaseSettings):
    app_name: str = "GrayLink"
    debug: bool = False
    config_file: str = "config/config.yml"
    monitor: MonitorSettings = MonitorSettings()
    symlink: SymlinkSettings = SymlinkSettings()
    emby: EmbySettings = EmbySettings()
    database: DatabaseSettings = DatabaseSettings()

    @classmethod
    def load_config(cls):
        config_path = os.getenv("CONFIG_FILE", "config/config.yml")
        
        # 如果配置文件不存在，创建默认配置
        if not os.path.exists(config_path):
            # 确保目录存在
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            # 创建默认配置实例
            default_config = cls()
            
            # 将默认配置保存到文件
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(
                    default_config.model_dump(),
                    f,
                    allow_unicode=True,
                    sort_keys=False
                )
            
            return default_config
            
        # 如果配置文件存在，读取配置
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
            
        return cls(**config_data)

settings = Settings.load_config() 