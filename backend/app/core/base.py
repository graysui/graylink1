"""基础模型模块

提供 SQLAlchemy 基础模型类和通用功能。
"""
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# 创建基础模型类
Base = declarative_base()

class BaseModel(Base):
    """基础模型类
    
    提供所有模型共用的基础字段和方法。
    """
    
    __abstract__ = True
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典
        
        Returns:
            包含模型数据的字典
        """
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int):
        """
        通过 ID 获取记录
        """
        return await session.get(cls, id)

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        """
        创建新记录
        """
        instance = cls(**kwargs)
        session.add(instance)
        await session.flush()
        await session.refresh(instance)
        return instance 