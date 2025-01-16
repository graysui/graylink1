# GrayLink

![Docker Build](https://github.com/graysui/graylink1/actions/workflows/docker-publish.yml/badge.svg)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/graysui/graylink1)

GrayLink 是一个高性能的 Google Drive 文件监控和软链接管理系统，支持 Docker 部署，采用前后端分离架构。本项目主要用于监控 Google Drive 目录变化，自动生成相应的软链接，并支持 Emby 媒体库自动刷新。

## 🌟 特性

- 🚀 高效的文件监控机制，支持增量扫描
- 🔌 集成 Google Drive API，实现精确的文件变更检测
- 🔗 智能的软链接管理，自动处理文件变更
- 🛡️ 完善的异常处理机制
- 📺 支持 Emby 媒体库自动刷新
- 🖥️ 友好的 Web 管理界面

## 🏗️ 项目结构

```
graylink/
├── frontend/                # 前端项目
│   └── graylink-web/       # Vue 3 + TypeScript 项目
│       ├── src/
│       │   ├── api/        # API 接口定义
│       │   ├── components/ # 通用组件
│       │   ├── stores/     # Pinia 状态管理
│       │   ├── types/      # TypeScript 类型定义
│       │   ├── utils/      # 工具函数
│       │   └── views/      # 页面组件
│       └── ...
└── backend/                # 后端项目
    ├── app/               # 应用核心模块
    │   ├── core/         # 核心功能模块
    │   │   ├── base.py   # SQLAlchemy 基类定义
    │   │   ├── database.py # 数据库连接管理
    │   │   ├── session.py # 会话管理
    │   │   ├── config.py # 配置管理
    │   │   ├── cache.py  # 缓存管理
    │   │   └── security.py # 安全相关
    │   ├── modules/      # 业务模块
    │   │   ├── monitor/  # 监控模块
    │   │   ├── symlink/  # 软链接模块
    │   │   ├── emby/     # Emby集成
    │   │   └── database/ # 数据库管理
    │   ├── handlers/     # API处理器
    │   ├── models/       # 数据模型
    │   ├── schemas/      # 数据验证
    │   └── utils/        # 工具函数
    ├── config/           # 配置文件目录
    ├── data/            # 数据存储目录
    └── logs/            # 日志目录
```

## 🚀 技术栈

### 前端技术栈
- Vue 3 + TypeScript
- Pinia 状态管理
- Vue Router
- Element Plus UI
- Vite 构建工具

### 后端技术栈
- Python FastAPI
- SQLAlchemy 异步 ORM
- SQLite 数据库
- Google Drive API
- Emby API

## 🛠️ 开发环境设置

### 前端开发
```bash
cd frontend/graylink-web
npm install
npm run dev
```

### 后端开发
```bash
cd backend
pip install -r requirements.txt
# 创建必要的目录
mkdir data logs
# 复制并修改配置文件
cp config/config.example.yml config/config.yml
# 启动服务
python -m uvicorn main:app --reload
```

## 🐳 Docker 部署

### 系统架构支持

镜像支持以下架构：
- `linux/amd64`: 适用于 Intel/AMD 处理器
- `linux/arm64`: 适用于 ARM 处理器（如 Apple M1/M2、树莓派等）

Docker 会自动选择适合您系统的版本。

### 从 Docker Hub 安装（推荐）

```bash
# 拉取最新版本
docker pull gray777/graylink:latest

# 或者指定版本
docker pull gray777/graylink:v1.0.0
```

### 使用 docker-compose

```yaml
version: '3'

services:
  graylink:
    image: gray777/graylink:latest
    ports:
      - "8728:8728"  # 前端端口
      - "8000:8000"  # 后端API端口
    volumes:
      - ./config:/app/backend/config  # 配置文件
      - ./data:/app/backend/data      # 数据目录
      - ./logs:/app/backend/logs      # 日志目录
      - /path/to/gdrive:/gdrive:shared  # Google Drive 目录
    environment:
      - TZ=Asia/Shanghai
    restart: unless-stopped
```

## ⚙️ 配置说明

### 基础配置
```yaml
app_name: "GrayLink"
debug: true
config_file: "config/config.yml"
```

### 监控配置
```yaml
monitor:
  scan_interval: 300  # 扫描间隔（秒）
  google_drive:
    client_id: ""     # Google Drive API 客户端 ID
    client_secret: "" # Google Drive API 客户端密钥
    token_file: "data/gdrive_token.json"
```

### 软链接配置
```yaml
symlink:
  source_dir: "D:/media/nastool"     # 媒体文件目录
  target_dir: "D:/nastool-nfo"       # NFO文件目录
  preserve_structure: true           # 保持目录结构
  backup_on_conflict: true          # 发生冲突时备份
```

### Emby配置
```yaml
emby:
  host: "http://localhost:8096"     # Emby服务器地址
  api_key: ""                       # Emby API密钥
  auto_refresh: true               # 自动刷新媒体库
  refresh_delay: 10                # 刷新延迟（秒）
```

### 数据库配置
```yaml
database:
  url: "sqlite+aiosqlite:///data/graylink.db"
  pool_size: 20
  max_overflow: 10
  pool_timeout: 30
  pool_recycle: 3600
  echo: false                      # 调试时可设为true
  batch_size: 1000
```