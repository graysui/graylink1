"""认证管理模块

提供用户认证和授权功能。
"""
from datetime import datetime, timedelta
from typing import Any, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.session import session_manager
from app.models.user import User

class AuthError(Exception):
    """认证错误"""
    pass

class AuthManager:
    """认证管理器
    
    提供用户认证、令牌管理等功能。
    """
    
    def __init__(self):
        """初始化认证管理器"""
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        
        # 性能统计
        self.total_auth_attempts = 0
        self.failed_auth_attempts = 0
        self._last_cleanup = datetime.now()
        
    @property
    def stats(self) -> dict:
        """获取认证统计信息"""
        total = self.total_auth_attempts
        failed = self.failed_auth_attempts
        return {
            "total_attempts": total,
            "failed_attempts": failed,
            "success_rate": (total - failed) / total if total > 0 else 0,
            "last_cleanup": self._last_cleanup.isoformat()
        }
        
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码
        
        Args:
            plain_password: 明文密码
            hashed_password: 哈希密码
            
        Returns:
            是否验证通过
        """
        return self.pwd_context.verify(plain_password, hashed_password)
        
    def get_password_hash(self, password: str) -> str:
        """获取密码哈希值
        
        Args:
            password: 明文密码
            
        Returns:
            密码哈希值
        """
        return self.pwd_context.hash(password)
        
    async def authenticate_user(
        self,
        username: str,
        password: str,
        db: AsyncSession
    ) -> Optional[User]:
        """认证用户
        
        Args:
            username: 用户名
            password: 密码
            db: 数据库会话
            
        Returns:
            认证通过的用户或 None
        """
        self.total_auth_attempts += 1
        try:
            user = await self._get_user_by_username(username, db)
            if not user:
                self.failed_auth_attempts += 1
                return None
                
            if not self.verify_password(password, user.hashed_password):
                self.failed_auth_attempts += 1
                return None
                
            return user
            
        except Exception as e:
            self.failed_auth_attempts += 1
            raise AuthError(f"认证失败: {str(e)}")
            
    def create_access_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """创建访问令牌
        
        Args:
            data: 令牌数据
            expires_delta: 过期时间
            
        Returns:
            JWT 令牌
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta
            if expires_delta
            else timedelta(minutes=settings.security.access_token_expire_minutes)
        )
        to_encode.update({"exp": expire})
        
        try:
            return jwt.encode(
                to_encode,
                settings.security.secret_key,
                algorithm=settings.security.algorithm
            )
        except Exception as e:
            raise AuthError(f"创建令牌失败: {str(e)}")
            
    async def get_current_user(
        self,
        token: str,
        db: AsyncSession
    ) -> Optional[User]:
        """获取当前用户
        
        Args:
            token: 访问令牌
            db: 数据库会话
            
        Returns:
            当前用户或 None
            
        Raises:
            AuthError: 认证失败
        """
        try:
            payload = jwt.decode(
                token,
                settings.security.secret_key,
                algorithms=[settings.security.algorithm]
            )
            username: str = payload.get("sub")
            if username is None:
                raise AuthError("无效的令牌")
                
            return await self._get_user_by_username(username, db)
            
        except JWTError as e:
            raise AuthError(f"解析令牌失败: {str(e)}")
            
    async def _get_user_by_username(
        self,
        username: str,
        db: AsyncSession
    ) -> Optional[User]:
        """根据用户名获取用户
        
        Args:
            username: 用户名
            db: 数据库会话
            
        Returns:
            用户或 None
        """
        try:
            result = await db.execute(
                User.__table__.select().where(User.username == username)
            )
            return result.scalar_one_or_none()
            
        except Exception as e:
            raise AuthError(f"获取用户失败: {str(e)}")

# 创建认证管理器实例
auth_manager = AuthManager()

# 创建 OAuth2 密码流认证
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 