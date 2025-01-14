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
    ├── handlers/         # 请求处理器
    ├── models/          # 数据模型
    ├── schemas/         # 数据验证模式
    └── utils/           # 工具函数
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
python main.py
```

## 🐳 Docker 部署

### 从 Docker Hub 安装（推荐）

```bash
# 拉取最新版本
docker pull gray777/graylink:latest

# 或者指定版本
docker pull gray777/graylink:v1.0.0
```

### 从 GitHub Packages 安装

```bash
# 登录到 GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u graysui --password-stdin

# 拉取镜像
docker pull ghcr.io/graysui/graylink1:latest
```

### 使用 docker-compose

```yaml
version: '3'

services:
  graylink:
    # 使用 Docker Hub 镜像
    image: graysui/graylink:latest
    # 或者使用 GitHub Container Registry 镜像
    # image: ghcr.io/graysui/graylink1:latest
    ports:
      - "8728:8728"
      - "8000:8000"
    volumes:
      - ./config:/app/backend/config
      - ./data:/app/backend/data
      - /path/to/gdrive:/gdrive:shared
    environment:
      - TZ=Asia/Shanghai
    restart: unless-stopped
```