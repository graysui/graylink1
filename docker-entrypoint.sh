#!/bin/bash

# 输出调试信息
echo "Starting services..."

# 检查前端文件
echo "Checking frontend files..."
ls -la /app/frontend/dist/

# 检查 nginx 配置
echo "Checking nginx configuration..."
nginx -t

# 启动 nginx
echo "Starting nginx..."
nginx

# 启动后端服务
echo "Starting backend service..."
cd /app/backend
python main.py 