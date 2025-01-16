# GrayLink 后端项目结构

## 目录结构

```
backend/
├── app/                    # 应用主目录
│   ├── core/              # 核心功能模块
│   │   ├── base.py        # SQLAlchemy 基类定义
│   │   ├── database.py    # 数据库连接管理
│   │   ├── session.py     # 会话生命周期管理
│   │   ├── config.py      # 配置管理
│   │   ├── cache.py       # 缓存管理
│   │   └── security.py    # 安全相关功能
│   │
│   ├── handlers/          # API 处理器
│   │   ├── auth.py        # 认证相关处理器
│   │   ├── monitor.py     # 监控相关处理器
│   │   └── ...
│   │
│   ├── models/            # 数据模型定义
│   │   ├── user.py        # 用户模型
│   │   └── ...
│   │
│   ├── modules/           # 业务模块
│   │   ├── monitor/       # 监控模块
│   │   │   ├── models.py  # 监控数据模型
│   │   │   ├── scanner.py # 文件扫描器
│   │   │   ├── service.py # 监控服务
│   │   │   └── events.py  # 事件处理
│   │   │
│   │   ├── symlink/       # 软链接模块
│   │   │   └── manager.py # 软链接管理器
│   │   │
│   │   ├── emby/          # Emby 集成模块
│   │   │   ├── client.py  # Emby 客户端
│   │   │   └── service.py # Emby 服务
│   │   │
│   │   └── database/      # 数据库管理模块
│   │       └── manager.py # 数据库管理器
│   │
│   ├── schemas/           # 数据验证模式
│   │   └── ...
│   │
│   └── utils/             # 工具函数
│       └── ...
│
├── config/                # 配置文件目录
│   └── config.yml        # 主配置文件
│
├── data/                  # 数据目录
│   ├── backup/           # 配置备份
│   └── ...
│
└── tests/                # 测试目录
    ├── unit/            # 单元测试
    └── integration/     # 集成测试

## 模块说明

### 核心模块 (core)

1. **base.py**
   - 提供 SQLAlchemy 基础模型类
   - 定义通用的模型方法和属性
   - 支持异步操作和类型注解

2. **database.py**
   - 管理数据库连接
   - 提供会话工厂
   - 实现连接池监控
   - 支持异步数据库操作

3. **session.py**
   - 管理数据库会话生命周期
   - 提供会话统计和监控
   - 实现自动清理机制
   - 支持事务管理

4. **config.py**
   - 管理应用配置
   - 支持环境变量覆盖
   - 提供配置验证
   - 实现配置备份和恢复

5. **cache.py**
   - 提供应用级缓存
   - 支持多种缓存策略
   - 实现性能监控
   - 自动清理过期数据

6. **security.py**
   - 处理认证和授权
   - 管理用户会话
   - 提供安全相关工具
   - 实现访问控制

### 业务模块 (modules)

1. **Monitor 模块**
   - 实现文件系统监控
   - 管理 Google Drive 同步
   - 处理文件变更事件
   - 提供监控统计

2. **Symlink 模块**
   - 管理符号链接
   - 提供备份和恢复
   - 实现性能监控
   - 处理文件系统交互

3. **Emby 模块**
   - 集成 Emby 媒体服务器
   - 管理媒体库刷新
   - 提供 API 客户端
   - 实现错误重试

4. **Database 模块**
   - 提供数据库管理功能
   - 实现查询优化
   - 管理数据迁移
   - 提供性能监控

## 依赖关系

1. **核心依赖**
   - `core.base` → `core.database`
   - `core.database` → `core.session`
   - `core.session` → `core.cache`
   - 所有模块 → `core.config`

2. **业务依赖**
   - `modules.monitor` → `modules.symlink`
   - `modules.monitor` → `modules.emby`
   - 所有业务模块 → `core.database`

## 开发规范

1. **导入规则**
   - 使用绝对导入
   - 避免循环依赖
   - 按类型分组导入
   - 保持导入顺序一致

2. **异步支持**
   - 所有 IO 操作使用异步
   - 提供异步上下文管理
   - 实现并发控制
   - 支持异步事件处理

3. **错误处理**
   - 使用自定义异常类
   - 提供详细错误信息
   - 实现错误重试机制
   - 确保异常安全

4. **性能考虑**
   - 实现缓存机制
   - 优化数据库查询
   - 控制并发级别
   - 监控关键指标 