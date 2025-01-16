"""
用户模型定义
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.core.base import BaseModel

class User(BaseModel):
    """
    用户模型
    包含用户的基本信息和认证信息
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(Text, nullable=False)  # 使用Text类型存储哈希后的密码
    role = Column(String(20), default="user", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 