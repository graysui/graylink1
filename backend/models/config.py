from pydantic import BaseModel, Field
from typing import Dict, Optional

class GoogleDriveConfig(BaseModel):
    # Active API 配置
    client_id: str = ""
    client_secret: str = ""
    token_file: str = "config/gdrive_token.json"
    refresh_token: Optional[str] = None
    watch_folder_id: str = ""  # 要监控的文件夹ID
    enabled: bool = False  # 是否启用活动监控
    check_interval: str = "1h"  # 检查间隔
    path_mapping: Dict[str, str] = Field(default_factory=dict)  # Drive路径映射到本地路径

class RcloneConfig(BaseModel):
    # rclone 配置
    config_file: str = "config/rclone.conf"
    remote_name: str = ""
    mount_point: str = "/mnt/media"
    mount_options: Dict[str, str] = Field(default_factory=dict)
    auto_mount: bool = False

class MonitorConfig(BaseModel):
    interval: int = Field(default=300, ge=60, le=3600)  # 本地监控间隔
    batch_size: int = Field(default=100, ge=10, le=1000)
    max_retries: int = Field(default=3, ge=1, le=10)
    google_drive: GoogleDriveConfig = Field(default_factory=GoogleDriveConfig)
    rclone: RcloneConfig = Field(default_factory=RcloneConfig)

class SymlinkConfig(BaseModel):
    source_dir: str
    target_dir: str
    preserve_structure: bool = True
    backup_on_conflict: bool = True
    conflict_strategy: str = Field(default="skip", pattern="^(skip|rename|overwrite)$")

class PasswordPolicy(BaseModel):
    min_length: int = Field(default=8, ge=6, le=32)
    require_special: bool = True
    require_numbers: bool = True

class SecurityConfig(BaseModel):
    max_login_attempts: int = Field(default=5, ge=1, le=10)
    session_timeout: int = Field(default=3600, ge=300)
    password_policy: PasswordPolicy

class EmbyConfig(BaseModel):
    host: str
    api_key: str = ""
    auto_refresh: bool = True
    refresh_delay: int = Field(default=10, ge=0)
    path_mapping: Dict[str, str] = {}

class SystemConfig(BaseModel):
    monitor: MonitorConfig
    symlink: SymlinkConfig
    emby: EmbyConfig
    security: SecurityConfig 