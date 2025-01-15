from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from models.user import User
from typing import Optional

router = APIRouter()

class LoginForm(BaseModel):
    username: str
    password: str

class ChangePasswordForm(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

async def get_user_by_username(username: str, db: AsyncSession) -> Optional[User]:
    """根据用户名获取用户"""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def authenticate_user(username: str, password: str, db: AsyncSession) -> Optional[User]:
    """验证用户"""
    user = await get_user_by_username(username, db)
    if not user or not User.verify_password(password, user.hashed_password):
        return None
    return user

@router.post("/login")
async def login(form: LoginForm, db: AsyncSession = Depends(get_db)):
    """登录接口"""
    user = await authenticate_user(form.username, form.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    return {
        "code": 0,
        "message": "登录成功",
        "data": {
            "token": "default-token",  # TODO: 实现JWT token
            "username": user.username,
            "userInfo": {
                "roles": ["admin"],
                "permissions": ["*"]
            }
        }
    }

@router.post("/change-password")
async def change_password(form: ChangePasswordForm, db: AsyncSession = Depends(get_db)):
    """修改密码接口"""
    # 获取当前用户（这里暂时使用默认用户名，后续应该从token中获取）
    user = await get_user_by_username("admin", db)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 验证旧密码
    if not User.verify_password(form.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="旧密码不正确")
    
    # 验证新密码和确认密码是否一致
    if form.new_password != form.confirm_password:
        raise HTTPException(status_code=400, detail="新密码和确认密码不一致")
    
    # 验证新密码长度
    if len(form.new_password) < 6:
        raise HTTPException(status_code=400, detail="新密码长度至少为6位")
    
    # 更新密码
    user.hashed_password = User.get_password_hash(form.new_password)
    db.add(user)
    await db.commit()
    
    return {
        "code": 0,
        "message": "密码修改成功"
    }

# 初始化默认用户
async def init_default_user(db: AsyncSession):
    """初始化默认用户"""
    user = await get_user_by_username("admin", db)
    if not user:
        default_user = User(
            username="admin",
            hashed_password=User.get_password_hash("admin")
        )
        db.add(default_user)
        await db.commit() 