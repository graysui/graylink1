# GrayLink

GrayLink 是一个高性能的 Google Drive 文件监控和软链接管理系统，支持 Docker 部署，采用前后端分离架构。本项目主要用于监控 Google Drive 目录变化，自动生成相应的软链接，并支持 Emby 媒体库自动刷新。

## 🌟 特性

- 🚀 高效的文件监控机制，支持增量扫描
- 🔌 集成 Google Drive API，实现精确的文件变更检测
- 🔗 智能的软链接管理，自动处理文件变更
- 🛡️ 完善的异常处理机制
- 📺 支持 Emby 媒体库自动刷新
- 🖥️ 友好的 Web 管理界面

## 🏗️ 系统架构

### 后端架构

采用模块化设计，核心模块包括：

#### 1. 监控模块 (Monitor)
- 文件系统实时监控
- Google Drive API 集成
- 智能增量扫描
- 事件驱动系统

#### 2. 数据库模块 (Database)
- SQLite 高性能存储
- 文件索引管理
- 目录结构快照生成

#### 3. 软链接管理模块 (Symlink)
- 智能软链接生成
- 冲突检测与处理
- 实时同步更新

#### 4. Emby 集成模块 (Emby)
- 媒体库自动管理
- API 深度集成
- 智能刷新机制

#### 5. 系统模块
- 日志记录与分析
- 异常检测与处理
- 配置管理中心

### 前端架构

基于现代化技术栈：
- Vue.js 3.0 + TypeScript
- Element Plus UI
- Pinia 状态管理
- Axios 请求处理

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- SQLite 3
- Docker & Docker Compose

### Docker 部署

```yaml
version: '3'
services:
  graylink-backend:
    build: ./backend
    volumes:
      - ./config:/app/config
      - ./data:/app/data
      - /path/to/gdrive:/gdrive:shared
    environment:
      - TZ=Asia/Shanghai
    restart: unless-stopped

  graylink-frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - graylink-backend
    restart: unless-stopped
```

### 手动部署

1. 克隆项目
```bash
git clone https://github.com/yourusername/graylink.git
cd graylink
```

2. 后端配置
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
cp config/config.example.yml config/config.yml
# 编辑 config.yml 配置文件
```

3. 前端配置
```bash
cd frontend
npm install
cp .env.example .env
# 编辑 .env 配置文件
```

4. 启动服务
```bash
# 后端
cd backend
python main.py

# 前端
cd frontend
npm run dev  # 开发环境
npm run build  # 生产环境
```

## 📝 配置说明

### 核心配置项

```yaml
monitor:
  scan_interval: 300  # 扫描间隔（秒）
  google_drive:
    client_id: "your_client_id"
    client_secret: "your_client_secret"
    
symlink:
  source_dir: "/gdrive/media"
  target_dir: "/data/media"
  
emby:
  host: "http://emby:8096"
  api_key: "your_api_key"
```

## 🔒 安全性设计

- API 认证与授权
- 数据加密存储
- 访问控制机制
- 安全日志记录

## 🎯 性能优化

- 异步 IO 处理
- 多线程任务处理
- 增量扫描机制
- 数据库索引优化
- 智能缓存策略

## 📖 文档

详细文档请参考：
- [安装指南](docs/installation.md)
- [配置手册](docs/configuration.md)
- [API 文档](docs/api.md)
- [常见问题](docs/faq.md)

## 🤝 贡献指南

欢迎提交 Pull Request 和 Issue。在提交之前，请确保：

1. 代码符合项目规范
2. 添加必要的测试用例
3. 更新相关文档
4. 提供清晰的提交信息

## 📄 许可证

[MIT License](LICENSE)

## 📮 联系方式

- 项目维护者：[维护者姓名]
- Email：[邮箱地址]
- GitHub：[GitHub地址]
- 问题反馈：[Issues](https://github.com/yourusername/graylink/issues)