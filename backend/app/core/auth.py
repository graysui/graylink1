"""认证管理模块

提供用户认证和授权功能。
"""
from datetime import datetime, timedelta
from typing import Any, Optional, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.models.user import User

# 配置密码上下文
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__ident="2b"
)

class AuthError(Exception):
    """认证错误"""
    pass

class AuthManager:
    """认证管理器
    
    提供用户认证和授权功能。
    """
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'AuthManager':
        """获取认证管理器实例（单例）"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        """初始化认证管理器"""
        # 认证统计
        self._total_auth_attempts = 0
        self._failed_auth_attempts = 0
        self._last_auth_time = None
        self._last_error = None
        
    @property
    def stats(self) -> Dict[str, Any]:
        """获取认证统计信息"""
        return {
            "total_auth_attempts": self._total_auth_attempts,
            "failed_auth_attempts": self._failed_auth_attempts,
            "success_rate": (self._total_auth_attempts - self._failed_auth_attempts) / self._total_auth_attempts if self._total_auth_attempts > 0 else 0,
            "last_auth_time": self._last_auth_time.isoformat() if self._last_auth_time else None,
            "last_error": str(self._last_error) if self._last_error else None
        }
        
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
        self._total_auth_attempts += 1
        self._last_auth_time = datetime.now()
        
        try:
            user = await self._get_user_by_username(username, db)
            if not user:
                self._failed_auth_attempts += 1
                return None
                
            if not self.verify_password(password, user.password):
                self._failed_auth_attempts += 1
                return None
                
            return user
            
        except Exception as e:
            self._failed_auth_attempts += 1
            self._last_error = str(e)
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
            self._last_error = str(e)
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
            self._last_error = str(e)
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
            from sqlalchemy.orm import selectinload
            stmt = (
                select(User)
                .where(User.username == username)
                .options(selectinload('*'))
            )
            result = await db.execute(stmt)
            return result.unique().scalar_one_or_none()
            
        except Exception as e:
            self._last_error = str(e)
            raise AuthError(f"获取用户失败: {str(e)}")
            
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码
        
        Args:
            plain_password: 明文密码
            hashed_password: 哈希密码
            
        Returns:
            是否验证通过
        """
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            self._last_error = str(e)
            raise AuthError(f"密码验证失败: {str(e)}")
            
    def get_password_hash(self, password: str) -> str:
        """获取密码哈希
        
        Args:
            password: 明文密码
            
        Returns:
            密码哈希
        """
        try:
            return pwd_context.hash(password)
        except Exception as e:
            self._last_error = str(e)
            raise AuthError(f"密码哈希失败: {str(e)}")

# 创建认证管理器实例
auth_manager = AuthManager.get_instance()

# 创建 OAuth2 密码流认证
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 顶层函数包装器
def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """创建访问令牌的包装函数"""
    return auth_manager.create_access_token(data, expires_delta)

def get_password_hash(password: str) -> str:
    """获取密码哈希的包装函数"""
    return auth_manager.get_password_hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码的包装函数"""
    return auth_manager.verify_password(plain_password, hashed_password) 