"""配置管理模块

提供应用配置管理，支持从文件和环境变量加载配置。
"""
import json
import os
import secrets
import stat
from datetime import datetime
from functools import lru_cache
from typing import Any, Dict, List, Optional

import yaml
from loguru import logger
from pydantic import BaseModel, Field, ValidationError, validator
from pydantic_settings import BaseSettings

class ConfigError(Exception):
    """配置错误"""
    pass

class GoogleDriveSettings(BaseModel):
    """Google Drive 配置"""
    client_id: str = Field(default="", description="Google Drive API 客户端ID")
    client_secret: str = Field(default="", description="Google Drive API 客户端密钥")
    token_file: str = Field(default="data/gdrive_token.json", description="Token 文件路径")
    
    @validator('token_file')
    def validate_token_file(cls, v):
        if not v:
            v = "data/gdrive_token.json"
        return os.path.normpath(v)

class MonitorSettings(BaseModel):
    """监控配置"""
    scan_interval: int = Field(default=300, description="扫描间隔（秒）", ge=60)
    google_drive: GoogleDriveSettings = Field(default_factory=GoogleDriveSettings, description="Google Drive 配置")
    
    @validator('scan_interval')
    def validate_scan_interval(cls, v):
        if v < 60:
            v = 300
        return v

class SymlinkSettings(BaseModel):
    """符号链接配置"""
    source_dir: str = Field(default="./media", description="源目录")
    target_dir: str = Field(default="./media-nfo", description="目标目录")
    preserve_structure: bool = Field(default=True, description="保持目录结构")
    backup_on_conflict: bool = Field(default=True, description="冲突时备份")
    backup_dir: str = Field(default="data/backup", description="备份目录")
    max_backups: int = Field(default=5, description="最大备份数", ge=1)
    
    @validator('source_dir', 'target_dir', 'backup_dir')
    def validate_directory(cls, v):
        if not v:
            if v == 'source_dir':
                v = "./media"
            elif v == 'target_dir':
                v = "./media-nfo"
            else:
                v = "data/backup"
        return os.path.normpath(v)

class EmbySettings(BaseModel):
    """Emby 配置"""
    server_url: str = Field(default="http://localhost:8096", description="Emby 服务器地址")
    api_key: Optional[str] = Field(default=None, description="Emby API 密钥")
    auto_refresh: bool = Field(default=True, description="自动刷新媒体库")
    refresh_delay: int = Field(default=10, description="刷新延迟（秒）", ge=1)
    path_mapping: Dict[str, str] = Field(default_factory=dict, description="路径映射")
    library_paths: List[str] = Field(default_factory=list, description="媒体库路径")
    timeout: int = Field(default=30, description="请求超时时间（秒）", ge=1)
    max_retries: int = Field(default=3, description="最大重试次数", ge=0)
    retry_delay: int = Field(default=5, description="重试延迟（秒）", ge=1)
    
    @validator('server_url')
    def validate_server_url(cls, v):
        if not v:
            v = "http://localhost:8096"
        return v.rstrip('/')

class DatabaseSettings(BaseModel):
    """数据库配置"""
    url: str = Field(default="sqlite+aiosqlite:///data/graylink.db", description="数据库URL")
    pool_size: int = Field(default=20, description="连接池大小", ge=1)
    max_overflow: int = Field(default=10, description="最大溢出连接数", ge=0)
    pool_timeout: int = Field(default=30, description="连接池超时时间", ge=1)
    pool_recycle: int = Field(default=3600, description="连接回收时间", ge=1)
    echo: bool = Field(default=False, description="是否打印SQL语句")
    batch_size: int = Field(default=1000, description="批处理大小", ge=1)
    
    @validator('url')
    def validate_url(cls, v):
        if not v:
            v = "sqlite+aiosqlite:///data/graylink.db"
        return v

class SecuritySettings(BaseModel):
    """安全配置"""
    secret_key: str = Field(default="", description="密钥")
    algorithm: str = Field(default="HS256", description="加密算法")
    access_token_expire_minutes: int = Field(default=30, description="访问令牌过期时间（分钟）", ge=1)
    
    @validator('secret_key')
    def validate_secret_key(cls, v):
        if not v:
            v = secrets.token_urlsafe(32)
        return v
        
    @validator('algorithm')
    def validate_algorithm(cls, v):
        allowed = ['HS256', 'HS384', 'HS512']
        if v not in allowed:
            v = 'HS256'
        return v

class CacheSettings(BaseModel):
    """缓存配置"""
    strategy: str = Field(default="ttl", description="缓存策略（ttl 或 lru）")
    default_ttl: int = Field(default=300, description="默认过期时间（秒）", ge=1)
    maxsize: int = Field(default=1000, description="最大缓存条目数", ge=1)
    cleanup_interval: int = Field(default=3600, description="清理间隔（秒）", ge=60)
    
    @validator('strategy')
    def validate_strategy(cls, v):
        allowed = ['ttl', 'lru']
        if v not in allowed:
            v = 'ttl'
        return v

class Settings(BaseSettings):
    """应用配置"""
    app_name: str = Field(default="GrayLink", description="应用名称")
    debug: bool = Field(default=False, description="调试模式")
    config_file: str = Field(default="config/config.yml", description="配置文件路径")
    monitor: MonitorSettings = Field(default_factory=MonitorSettings, description="监控配置")
    symlink: SymlinkSettings = Field(default_factory=SymlinkSettings, description="符号链接配置")
    emby: EmbySettings = Field(default_factory=EmbySettings, description="Emby 配置")
    database: DatabaseSettings = Field(default_factory=DatabaseSettings, description="数据库配置")
    security: SecuritySettings = Field(default_factory=SecuritySettings, description="安全配置")
    cache: CacheSettings = Field(default_factory=CacheSettings, description="缓存配置")
    
    # 配置元数据
    _config_loaded_at: datetime = None
    _config_source: str = None
    _config_backup_path: str = None
    
    class Config:
        env_prefix = "GRAYLINK_"
        env_nested_delimiter = "__"
        
    @property
    def metadata(self) -> Dict[str, Any]:
        """获取配置元数据"""
        return {
            "loaded_at": self._config_loaded_at.isoformat() if self._config_loaded_at else None,
            "source": self._config_source,
            "backup_path": self._config_backup_path
        }
    
    @classmethod
    def ensure_directory(cls, path: str, mode: int = 0o755):
        """确保目录存在并设置正确的权限"""
        try:
            if not os.path.exists(path):
                os.makedirs(path, mode=mode, exist_ok=True)
            else:
                current_mode = stat.S_IMODE(os.stat(path).st_mode)
                if current_mode != mode:
                    os.chmod(path, mode)
        except Exception as e:
            logger.error(f"创建目录失败 [{path}]: {str(e)}")
    
    @classmethod
    def ensure_data_directory(cls):
        """确保数据目录存在"""
        cls.ensure_directory("data")
        cls.ensure_directory("config")
        cls.ensure_directory("data/backup")
    
    def backup_config(self) -> str:
        """备份当前配置
        
        Returns:
            备份文件路径
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = "data/backup"
            backup_path = os.path.join(backup_dir, f"config_{timestamp}.yml")
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(
                    self.model_dump(exclude={'_config_loaded_at', '_config_source', '_config_backup_path'}),
                    f,
                    allow_unicode=True,
                    sort_keys=False
                )
            
            self._config_backup_path = backup_path
            return backup_path
            
        except Exception as e:
            logger.error(f"备份配置失败: {str(e)}")
            return None
    
    def save_config(self) -> bool:
        """保存当前配置
        
        Returns:
            是否保存成功
        """
        try:
            # 先备份当前配置
            self.backup_config()
            
            # 保存新配置
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.safe_dump(
                    self.model_dump(exclude={'_config_loaded_at', '_config_source', '_config_backup_path'}),
                    f,
                    allow_unicode=True,
                    sort_keys=False
                )
            
            return True
            
        except Exception as e:
            logger.error(f"保存配置失败: {str(e)}")
            return False
    
    @classmethod
    def load_config(cls) -> 'Settings':
        """加载配置
        
        Returns:
            配置实例
        """
        try:
            # 确保必要的目录存在
            cls.ensure_data_directory()
            
            config_path = os.getenv("GRAYLINK_CONFIG_FILE", "config/config.yml")
            
            # 如果配置文件不存在，使用默认配置
            if not os.path.exists(config_path):
                logger.warning("配置文件不存在，使用默认配置")
                return cls()
                
            # 加载配置文件
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
                
            # 创建配置实例
            settings = cls(**config_data)
            settings._config_loaded_at = datetime.now()
            settings._config_source = config_path
            
            return settings
            
        except Exception as e:
            logger.error(f"加载配置失败: {str(e)}")
            logger.warning("使用默认配置")
            return cls()

# 创建全局配置实例
settings = Settings.load_config() 