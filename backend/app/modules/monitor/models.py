from sqlalchemy import Column, Integer, String, DateTime, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class FileRecord(Base):
    __tablename__ = "file_records"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, index=True)
    file_id = Column(String, index=True)  # Google Drive file ID
    modified_time = Column(DateTime)
    size = Column(Integer)
    is_directory = Column(Boolean, default=False)
    last_checked = Column(DateTime, default=datetime.utcnow)
    
    # 添加索引以优化查询性能
    __table_args__ = (
        Index('idx_file_id', 'file_id'),  # 文件ID索引
        Index('idx_path', 'path'),        # 路径索引
        Index('idx_last_checked', 'last_checked'),  # 最后检查时间索引
        Index('idx_modified', 'modified_time'),     # 修改时间索引
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "path": self.path,
            "file_id": self.file_id,
            "modified_time": self.modified_time.isoformat() if self.modified_time else None,
            "size": self.size,
            "is_directory": self.is_directory,
            "last_checked": self.last_checked.isoformat() if self.last_checked else None
        } 