"""
用户模型定义
"""
from sqlalchemy import Column, Integer, String
from app.core.base import BaseModel

class User(BaseModel):
    """
    用户模型
    包含用户的基本信息和认证信息
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user") 