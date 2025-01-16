"""安全管理模块

提供安全相关功能，包括认证、授权和访问控制。
"""
from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.auth import auth_manager, oauth2_scheme
from app.models.user import User

class SecurityError(Exception):
    """安全错误"""
    pass

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前用户
    
    Args:
        token: 访问令牌
        db: 数据库会话
        
    Returns:
        当前用户
        
    Raises:
        HTTPException: 认证失败
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        user = await auth_manager.get_current_user(token, db)
        if user is None:
            raise credentials_exception
        return user
    except Exception as e:
        raise credentials_exception

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前活动用户
    
    Args:
        current_user: 当前用户
        
    Returns:
        当前活动用户
        
    Raises:
        HTTPException: 用户未激活
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户未激活"
        )
    return current_user

async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前超级用户
    
    Args:
        current_user: 当前用户
        
    Returns:
        当前超级用户
        
    Raises:
        HTTPException: 权限不足
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    return current_user 