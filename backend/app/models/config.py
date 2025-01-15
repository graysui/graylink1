from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class DriveConfig(BaseModel):
    enabled: bool = False
    client_id: str = ""
    client_secret: str = ""
    token_file: str = "data/gdrive_token.json"
    watch_folder_id: str = ""
    check_interval: str = "1h"
    path_mapping: Dict[str, str] = Field(default_factory=dict)

class MonitorConfig(BaseModel):
    scan_interval: int = 300
    watch_paths: List[str] = Field(default_factory=list)
    excluded_paths: List[str] = Field(default_factory=list)
    google_drive: DriveConfig = Field(default_factory=DriveConfig)

class SymlinkConfig(BaseModel):
    source_dir: str = "/mnt/media/nastool"
    target_dir: str = "/mnt/nastool-nfo"
    preserve_structure: bool = True
    backup_on_conflict: bool = True

class EmbyConfig(BaseModel):
    host: str = "http://emby:8096"
    api_key: str = ""
    auto_refresh: bool = True
    refresh_delay: int = 10
    path_mapping: Dict[str, str] = Field(default_factory=dict)

class PasswordPolicy(BaseModel):
    min_length: int = 8
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_numbers: bool = True
    require_special: bool = True

class SecurityConfig(BaseModel):
    password_policy: PasswordPolicy = Field(default_factory=PasswordPolicy)

class SystemConfig(BaseModel):
    app_name: str = "GrayLink"
    debug: bool = True
    config_file: str = "config/config.yml"
    monitor: MonitorConfig = Field(default_factory=MonitorConfig)
    symlink: SymlinkConfig = Field(default_factory=SymlinkConfig)
    emby: EmbyConfig = Field(default_factory=EmbyConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    database: dict = Field(default_factory=lambda: {
        "url": "sqlite+aiosqlite:///data/graylink.db",
        "pool_size": 20,
        "max_overflow": 10,
        "pool_timeout": 30,
        "pool_recycle": 3600,
        "echo": False,
        "batch_size": 1000
    }) 