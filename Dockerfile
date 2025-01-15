# 使用多阶段构建
# 前端构建阶段
FROM node:18-alpine as frontend-builder
WORKDIR /app

# 首先只复制 package.json 和 package-lock.json
COPY frontend/graylink-web/package*.json ./

# 安装依赖
RUN npm install

# 复制其余前端源代码
COPY frontend/graylink-web/ .

# 显示目录内容以进行调试
RUN ls -la

# 设置生产环境变量
ENV NODE_ENV=production
ENV VITE_APP_API_BASE_URL=/api

# 运行构建命令并添加详细输出
RUN npm run build --verbose

# 验证构建输出
RUN ls -la dist/

# 后端构建阶段
FROM python:3.11-slim as backend-builder
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 最终镜像
FROM python:3.11-slim
WORKDIR /app

# 安装必要的工具和nginx
RUN apt-get update && \
    apt-get install -y nginx procps && \
    rm -rf /var/lib/apt/lists/*

# 创建必要的目录
RUN mkdir -p /app/frontend/dist /app/backend /var/log/nginx

# 复制前端构建产物
COPY --from=frontend-builder /app/dist /app/frontend/dist
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 验证前端文件并设置权限
RUN ls -la /app/frontend/dist/ && \
    chown -R www-data:www-data /app/frontend/dist

# 复制后端代码和依赖
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY backend/ /app/backend/

# 复制启动脚本并设置权限
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh && \
    chown -R www-data:www-data /var/log/nginx

# 设置工作目录权限
RUN chown -R www-data:www-data /app

# 暴露端口
EXPOSE 8728 8000

# 启动服务
ENTRYPOINT ["/app/docker-entrypoint.sh"] 