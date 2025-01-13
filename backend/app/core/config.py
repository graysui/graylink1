from pydantic_settings import BaseSettings
from pydantic import BaseModel
from typing import Optional, Dict
import yaml
import os

class GoogleDriveSettings(BaseModel):
    client_id: str
    client_secret: str
    token_file: str

class MonitorSettings(BaseModel):
    scan_interval: int = 300
    google_drive: GoogleDriveSettings

class SymlinkSettings(BaseModel):
    source_dir: str
    target_dir: str
    preserve_structure: bool = True
    backup_on_conflict: bool = True

class EmbySettings(BaseModel):
    host: str
    api_key: str
    auto_refresh: bool = True
    refresh_delay: int = 10
    path_mapping: Dict[str, str] = {}

class DatabaseSettings(BaseModel):
    url: str
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
    monitor: MonitorSettings
    symlink: SymlinkSettings
    emby: EmbySettings
    database: DatabaseSettings

    @classmethod
    def load_config(cls):
        config_path = os.getenv("CONFIG_FILE", "config/config.yml")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
            
        return cls(**config_data)

settings = Settings.load_config() 