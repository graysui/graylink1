# GrayLink 后端关键任务

## 1. 认证模块
- [x] 创建 auth.py 处理器
- [x] 实现用户模型
- [x] 实现 JWT 认证
- [x] 添加安全配置

## 2. 配置系统
- [x] 基础配置结构
- [x] 配置文件加载
- [ ] 配置验证和默认值
  - [x] 基础配置文件创建功能
  - [ ] 确保配置目录存在
  - [ ] 验证数据目录是否存在并创建
  - [ ] 验证必要的配置项（security.secret_key 等）
  - [ ] 确保文件权限正确

说明：
1. 配置文件不存在时自动创建默认配置
2. 验证关键目录和文件的存在性
3. 确保敏感配置项有合适的值

## 3. 数据库
- [x] 基础数据库配置
- [x] 用户表创建

## 4. API 处理器修复
- [x] auth 处理器
- [ ] 检查前端 monitor API 调用并修复对应后端接口
- [ ] 检查前端 file API 调用并修复对应后端接口
- [ ] 检查前端 symlink API 调用并修复对应后端接口
- [ ] 检查前端 emby API 调用并修复对应后端接口
- [ ] 检查前端 gdrive API 调用并修复对应后端接口

## 5. 错误处理
- [ ] 根据前端错误处理方式统一后端响应格式

## 6. 日志
- [ ] 添加基本错误日志，方便排查问题

## 优先级任务
1. 完善配置验证，确保默认配置文件正确创建
2. 修复后端 API 接口与前端调用不匹配的问题
3. 统一错误响应格式
4. 添加错误日志

## 遇到的问题
1. auth 模块缺失导致的导入错误
2. 配置文件验证缺失可能导致运行时错误
3. 后端接口与前端调用不匹配

## 下一步计划
1. 完善配置验证功能
2. 检查前端 monitor API 的具体调用方式
3. 修复后端 monitor 接口以匹配前端调用

## 待修复问题

### 1. handlers 模块导入错误修复计划

#### 问题描述
- 在 `main.py` 中无法导入 handlers 模块
- 错误信息：`ModuleNotFoundError: No module named 'handlers'`
- 当前导入语句：`from handlers import auth, monitor, file, symlink, emby, gdrive`

#### 修复思路

1. Python 包结构检查
   - [ ] 确认 handlers 目录是否存在于正确的位置
   - [ ] 检查 handlers 目录中是否包含 `__init__.py` 文件
   - [ ] 验证所有需要导入的模块文件是否存在

2. 项目结构调整
   - [ ] 将 handlers 目录移动到 app 包内
   - [ ] 更新导入语句为 `from app.handlers import auth, monitor, file, symlink, emby, gdrive`
   - [ ] 确保 app 目录中有 `__init__.py` 文件

3. Docker 相关检查
   - [ ] 检查 Dockerfile 中的 COPY 命令是否正确复制了所有必要文件
   - [ ] 验证 Docker 容器中的目录结构
   - [ ] 确认 Python 路径设置是否正确

4. 依赖管理
   - [ ] 检查 requirements.txt 中的依赖版本
   - [ ] 确保所有必要的依赖都已安装
   - [ ] 验证没有依赖冲突

#### 执行计划

1. 目录结构重组
```
backend/
├── app/
│   ├── __init__.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── monitor.py
│   │   ├── file.py
│   │   ├── symlink.py
│   │   ├── emby.py
│   │   └── gdrive.py
│   ├── models/
│   ├── schemas/
│   └── core/
├── main.py
└── requirements.txt
```

2. 代码修改步骤
   - [ ] 移动 handlers 目录到 app 包内
   - [ ] 更新所有相关的导入语句
   - [ ] 检查并修复可能受影响的相对导入
   - [ ] 更新 main.py 中的导入语句

3. Docker 配置更新
   - [ ] 更新 Dockerfile 中的 COPY 命令
   - [ ] 添加 PYTHONPATH 环境变量设置
   - [ ] 确保正确复制所有必要文件

4. 测试计划
   - [ ] 在本地环境测试导入
   - [ ] 在 Docker 环境中测试导入
   - [ ] 运行完整的应用程序测试
   - [ ] 验证所有 API 端点

#### 后续工作

1. 文档更新
   - [ ] 更新项目结构文档
   - [ ] 更新开发环境设置指南
   - [ ] 更新部署文档

2. 代码优化
   - [ ] 检查并优化其他可能的导入问题
   - [ ] 确保代码结构符合最佳实践
   - [ ] 添加必要的注释和文档字符串 