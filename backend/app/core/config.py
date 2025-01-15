from pydantic_settings import BaseSettings
from pydantic import BaseModel, validator
from typing import Optional, Dict
import yaml
import os
import secrets
import stat

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

class SecuritySettings(BaseModel):
    secret_key: str = ""
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @validator('secret_key')
    def validate_secret_key(cls, v):
        if not v:
            # 如果密钥为空，生成一个新的
            return secrets.token_urlsafe(32)
        return v

class Settings(BaseSettings):
    app_name: str = "GrayLink"
    debug: bool = False
    config_file: str = "config/config.yml"
    monitor: MonitorSettings = MonitorSettings()
    symlink: SymlinkSettings = SymlinkSettings()
    emby: EmbySettings = EmbySettings()
    database: DatabaseSettings = DatabaseSettings()
    security: SecuritySettings = SecuritySettings()

    @classmethod
    def ensure_directory(cls, path: str, mode: int = 0o755):
        """确保目录存在并设置正确的权限"""
        if not os.path.exists(path):
            os.makedirs(path, mode=mode, exist_ok=True)
        else:
            # 检查权限
            current_mode = stat.S_IMODE(os.stat(path).st_mode)
            if current_mode != mode:
                os.chmod(path, mode)

    @classmethod
    def ensure_data_directory(cls):
        """确保数据目录存在"""
        cls.ensure_directory("data")
        cls.ensure_directory("config")

    @classmethod
    def load_config(cls):
        # 确保必要的目录存在
        cls.ensure_data_directory()
        
        config_path = os.getenv("CONFIG_FILE", "config/config.yml")
        
        # 如果配置文件不存在，创建默认配置
        if not os.path.exists(config_path):
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