#!/bin/bash

# 启用错误检测
set -e

# 输出调试信息
echo "Starting services..."
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

# 检查前端文件
echo "Checking frontend files..."
if [ -d "/app/frontend/dist" ]; then
    echo "Frontend dist directory exists"
    ls -la /app/frontend/dist/
    
    # 检查关键文件
    if [ ! -f "/app/frontend/dist/index.html" ]; then
        echo "ERROR: index.html not found!"
        exit 1
    fi
    
    # 检查index.html内容
    echo "Checking index.html content..."
    cat /app/frontend/dist/index.html
    
    # 检查assets目录
    echo "Checking assets directory..."
    ls -la /app/frontend/dist/assets/
else
    echo "ERROR: Frontend dist directory not found!"
    exit 1
fi

# 检查 nginx 配置
echo "Checking nginx configuration..."
nginx -t

# 确保日志目录存在
echo "Creating log directories..."
mkdir -p /var/log/nginx
touch /var/log/nginx/error.log
touch /var/log/nginx/access.log
chown -R www-data:www-data /var/log/nginx

# 启动 nginx
echo "Starting nginx..."
nginx
echo "Nginx started successfully"

# 检查nginx是否正在运行
if pgrep nginx > /dev/null; then
    echo "Nginx is running"
    # 检查nginx访问
    echo "Testing nginx..."
    curl -v http://localhost:8728/
else
    echo "ERROR: Nginx failed to start"
    exit 1
fi

# 启动后端服务
echo "Starting backend service..."
cd /app/backend
echo "Backend directory contents:"
ls -la
python main.py 