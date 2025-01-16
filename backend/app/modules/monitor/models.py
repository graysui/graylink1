"""
监控模块的数据模型定义

提供文件监控相关的数据模型。
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Index, event
from sqlalchemy.orm import validates
from datetime import datetime
from typing import Dict, Optional
from app.core.base import BaseModel
from app.core.cache import cached

class FileRecord(BaseModel):
    """
    文件记录模型
    用于跟踪 Google Drive 文件的状态和变更历史。
    """
    __tablename__ = "file_records"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, index=True, nullable=False)
    file_id = Column(String, index=True, nullable=False)  # Google Drive file ID
    modified_time = Column(DateTime, nullable=False)
    size = Column(Integer, default=0)
    is_directory = Column(Boolean, default=False)
    last_checked = Column(DateTime, default=datetime.utcnow)
    mime_type = Column(String)  # 文件MIME类型
    
    # 添加索引以优化查询性能
    __table_args__ = (
        Index('idx_file_id', 'file_id'),  # 文件ID索引
        Index('idx_path', 'path'),        # 路径索引
        Index('idx_last_checked', 'last_checked'),  # 最后检查时间索引
        Index('idx_modified', 'modified_time'),     # 修改时间索引
        {"extend_existing": True}  # 允许模型更新
    )
    
    @validates('path')
    def validate_path(self, key: str, path: str) -> str:
        """验证路径格式"""
        if not path:
            raise ValueError("路径不能为空")
        # 规范化路径分隔符
        return path.replace('\\', '/')
    
    @validates('file_id')
    def validate_file_id(self, key: str, file_id: str) -> str:
        """验证文件ID"""
        if not file_id:
            raise ValueError("文件ID不能为空")
        return file_id
    
    @property
    def is_media_file(self) -> bool:
        """判断是否为媒体文件"""
        media_types = {
            'video': ['mp4', 'mkv', 'avi', 'mov'],
            'audio': ['mp3', 'wav', 'flac'],
            'image': ['jpg', 'jpeg', 'png', 'gif']
        }
        ext = self.path.split('.')[-1].lower() if '.' in self.path else ''
        return any(ext in types for types in media_types.values())
    
    @property
    def file_type(self) -> str:
        """获取文件类型"""
        if self.is_directory:
            return 'directory'
        ext = self.path.split('.')[-1].lower() if '.' in self.path else ''
        if not ext:
            return 'unknown'
        # 根据扩展名判断文件类型
        type_map = {
            'video': ['mp4', 'mkv', 'avi', 'mov'],
            'audio': ['mp3', 'wav', 'flac'],
            'image': ['jpg', 'jpeg', 'png', 'gif'],
            'document': ['pdf', 'doc', 'docx', 'txt'],
            'archive': ['zip', 'rar', '7z']
        }
        for file_type, extensions in type_map.items():
            if ext in extensions:
                return file_type
        return 'other'
    
    @cached(prefix="file_record", ttl=300)
    async def get_parent_path(self) -> Optional[str]:
        """获取父目录路径"""
        if '/' not in self.path:
            return None
        return '/'.join(self.path.split('/')[:-1])
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "id": self.id,
            "path": self.path,
            "file_id": self.file_id,
            "modified_time": self.modified_time.isoformat() if self.modified_time else None,
            "size": self.size,
            "is_directory": self.is_directory,
            "last_checked": self.last_checked.isoformat() if self.last_checked else None,
            "mime_type": self.mime_type,
            "file_type": self.file_type,
            "is_media_file": self.is_media_file
        }

@event.listens_for(FileRecord, 'before_update')
def update_last_checked(mapper, connection, target):
    """更新记录时自动更新最后检查时间"""
    target.last_checked = datetime.utcnow() 