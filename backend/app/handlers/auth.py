from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserProfile
from app.core.auth import (
    create_access_token,
    get_password_hash,
    verify_password,
    auth_manager,
    oauth2_scheme
)
from typing import Optional

router = APIRouter()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前用户"""
    try:
        return await auth_manager.get_current_user(token, db)
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """根据用户名获取用户"""
    result = await db.execute(User.__table__.select().where(User.username == username))
    return result.scalar_one_or_none()

async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
    """验证用户"""
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

@router.post("/login")
async def login(form_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """用户登录"""
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    access_token = create_access_token(data={"sub": user.username})
    return {
        "code": 0,
        "data": {
            "username": user.username,
            "role": user.role
        },
        "message": "登录成功",
        "token": access_token
    }

@router.post("/register")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    db_user = await get_user_by_username(db, user_data.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 创建新用户
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        password=hashed_password,
        role="user"  # 新注册用户默认为普通用户
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return {
        "code": 0,
        "data": None,
        "message": "注册成功"
    }

@router.post("/logout")
async def logout():
    """用户登出"""
    return {
        "code": 0,
        "data": None,
        "message": "登出成功"
    }

@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    """获取用户信息"""
    return {
        "code": 0,
        "data": {
            "username": current_user.username,
            "role": current_user.role,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
            "updated_at": current_user.updated_at.isoformat() if current_user.updated_at else None
        },
        "message": "获取成功"
    }

@router.post("/profile")
async def update_profile(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新用户信息"""
    # 如果要修改用户名，检查新用户名是否已存在
    if user_data.username != current_user.username:
        db_user = await get_user_by_username(db, user_data.username)
        if db_user:
            raise HTTPException(status_code=400, detail="用户名已存在")
        current_user.username = user_data.username
    
    # 更新密码
    if user_data.password:
        current_user.password = get_password_hash(user_data.password)
    
    await db.commit()
    await db.refresh(current_user)
    
    return {
        "code": 0,
        "data": None,
        "message": "更新成功"
    }

async def init_default_user(db: AsyncSession):
    """初始化默认用户"""
    # 检查是否已存在默认用户
    default_user = await get_user_by_username(db, "admin")
    if default_user:
        return
    
    # 创建默认用户
    hashed_password = get_password_hash("admin")
    default_user = User(
        username="admin",
        password=hashed_password,
        role="admin"  # 默认管理员用户
    )
    db.add(default_user)
    await db.commit() 