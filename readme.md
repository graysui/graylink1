# GrayLink

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

使用 Docker Compose 一键部署：
```bash
docker-compose up -d
```

## 📝 配置说明

### 前端配置
- `.env.development`: 开发环境配置
- `.env.production`: 生产环境配置

### 后端配置
- `config/`: 配置文件目录
  - `app.yaml`: 应用配置
  - `google.yaml`: Google Drive 配置
  - `emby.yaml`: Emby 配置

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 发起 Pull Request

## 📄 许可证

本项目采用 MIT 许可证