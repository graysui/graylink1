# GrayLink 后端开发指南

## 开发环境设置

### 1. 环境要求
- Python 3.9+
- pip 或 poetry
- SQLite 或 PostgreSQL
- Git

### 2. 安装依赖
```bash
# 使用 pip
pip install -r requirements.txt

# 或使用 poetry
poetry install
```

### 3. 配置文件
```bash
# 复制配置模板
cp config/config.example.yml config/config.yml

# 编辑配置文件
vim config/config.yml
```

## 开发规范

### 1. 代码风格
- 遵循 PEP 8 规范
- 使用 4 空格缩进
- 行长度限制在 88 字符
- 使用类型注解
- 添加详细的文档字符串

### 2. 导入规范
```python
# 标准库导入
import os
import sys
from typing import Optional, List

# 第三方库导入
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

# 本地模块导入
from app.core.config import settings
from app.models.user import User
```

### 3. 异步编程
```python
# 异步函数定义
async def get_user(user_id: int) -> Optional[User]:
    async with session_manager.session() as session:
        return await session.get(User, user_id)

# 异步上下文管理
async with session_manager.session() as session:
    try:
        result = await session.execute(query)
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise
```

### 4. 错误处理
```python
# 自定义异常类
class DatabaseError(Exception):
    pass

# 错误处理
try:
    await operation()
except Exception as e:
    logger.error(f"操作失败: {str(e)}")
    raise DatabaseError(f"数据库操作失败: {str(e)}")
```

## 模块开发指南

### 1. 创建新模块
```
modules/
└── new_module/
    ├── __init__.py
    ├── models.py      # 数据模型
    ├── service.py     # 业务逻辑
    └── manager.py     # 管理功能
```

### 2. 数据模型定义
```python
from app.core.base import BaseModel
from sqlalchemy import Column, String, Integer

class NewModel(BaseModel):
    """新模型类
    
    提供新功能的数据模型。
    """
    __tablename__ = "new_models"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
```

### 3. 服务实现
```python
class NewService:
    """新服务类
    
    提供新功能的业务逻辑实现。
    """
    
    def __init__(self, config: Config):
        self.config = config
        
    async def start(self):
        """启动服务"""
        pass
        
    async def stop(self):
        """停止服务"""
        pass
```

## API 开发指南

### 1. 创建新路由
```python
from fastapi import APIRouter, Depends
from app.core.database import get_db

router = APIRouter(prefix="/api/v1/new")

@router.get("/{item_id}")
async def get_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取项目详情"""
    pass
```

### 2. 请求验证
```python
from pydantic import BaseModel, Field

class ItemCreate(BaseModel):
    """创建项目请求模型"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
```

### 3. 响应处理
```python
from typing import List
from fastapi import HTTPException

@router.get("/")
async def list_items() -> List[Item]:
    """获取项目列表"""
    try:
        return await get_items()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取项目列表失败: {str(e)}"
        )
```

## 测试指南

### 1. 单元测试
```python
import pytest
from app.models.user import User

@pytest.mark.asyncio
async def test_create_user():
    """测试创建用户"""
    user = await User.create(
        username="test",
        email="test@example.com"
    )
    assert user.id is not None
    assert user.username == "test"
```

### 2. 集成测试
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    """测试主页"""
    response = client.get("/")
    assert response.status_code == 200
```

## 部署指南

### 1. 环境准备
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置设置
```bash
# 设置环境变量
export GRAYLINK_ENV=production
export GRAYLINK_DATABASE__URL=postgresql+asyncpg://user:pass@host/db
```

### 3. 启动服务
```bash
# 使用 uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# 或使用 gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 性能优化

### 1. 数据库优化
- 使用批量操作
- 优化查询语句
- 添加适当的索引
- 实现查询缓存

### 2. 缓存策略
- 使用 Redis 缓存
- 实现本地缓存
- 设置合理的过期时间
- 监控缓存命中率

### 3. 并发处理
- 控制并发级别
- 使用连接池
- 实现任务队列
- 优化锁机制

## 监控和日志

### 1. 日志配置
```python
import logging
from loguru import logger

logger.add(
    "logs/app.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO"
)
```

### 2. 性能监控
- 记录慢查询
- 监控内存使用
- 跟踪 API 响应时间
- 统计并发连接数

### 3. 告警机制
- 设置错误告警
- 监控系统资源
- 跟踪业务指标
- 发送告警通知

## 安全建议

### 1. 认证和授权
- 实现 JWT 认证
- 使用 HTTPS
- 实现角色权限
- 防止 CSRF 攻击

### 2. 数据安全
- 加密敏感数据
- 实现数据备份
- 控制访问权限
- 记录操作日志

### 3. 代码安全
- 避免 SQL 注入
- 验证用户输入
- 限制文件上传
- 保护配置信息
``` 