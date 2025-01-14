# 使用多阶段构建
# 前端构建阶段
FROM node:18-alpine as frontend-builder
WORKDIR /app
COPY frontend/graylink-web/package*.json ./
RUN npm install
COPY frontend/graylink-web/ .
RUN npm run build

# 后端构建阶段
FROM python:3.11-slim as backend-builder
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 最终镜像
FROM python:3.11-slim
WORKDIR /app

# 安装 nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# 复制前端构建产物
COPY --from=frontend-builder /app/dist /app/frontend/dist
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 复制后端代码和依赖
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY backend/ /app/backend/

# 复制启动脚本
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# 暴露端口
EXPOSE 8728 8000

# 启动服务
ENTRYPOINT ["/app/docker-entrypoint.sh"] 