from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class DriveConfig(BaseModel):
    enabled: bool = False
    client_id: str
    client_secret: str
    token_file: str = "data/gdrive_token.json"
    watch_folder_id: str
    check_interval: str = "1h"
    path_mapping: Dict[str, str] = {}

class MonitorConfig(BaseModel):
    scan_interval: int = 300
    watch_paths: List[str] = []
    excluded_paths: List[str] = []
    google_drive: DriveConfig = Field(default_factory=DriveConfig)

class SystemConfig(BaseModel):
    server: dict
    monitor: MonitorConfig = Field(default_factory=MonitorConfig)
    database: dict 