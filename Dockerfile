# 使用多阶段构建
# 前端构建阶段
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend

# 复制前端项目文件
COPY frontend/graylink-web/.env* ./
COPY frontend/graylink-web/package*.json ./
COPY frontend/graylink-web/tsconfig*.json ./
COPY frontend/graylink-web/vite.config.ts ./
COPY frontend/graylink-web/index.html ./
COPY frontend/graylink-web/env.d.ts ./
COPY frontend/graylink-web/vitest.config.ts ./
COPY frontend/graylink-web/eslint.config.js ./

# 安装依赖
RUN npm install

# 复制源代码
COPY frontend/graylink-web/src ./src
COPY frontend/graylink-web/public ./public

# 设置生产环境变量
ENV NODE_ENV=production
ENV VITE_APP_API_BASE_URL=/api

# 构建
RUN npm run build

# 后端构建阶段
FROM python:3.11-slim AS backend-builder
WORKDIR /app/backend

# 安装编译依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 复制并安装依赖
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt -v

# 复制后端源代码
COPY backend/app ./app
COPY backend/config ./config
COPY backend/middleware ./middleware
COPY backend/schemas ./schemas
COPY backend/main.py ./
COPY backend/__init__.py ./

# 最终镜像
FROM python:3.11-slim
WORKDIR /app

# 安装必要的工具和nginx
RUN apt-get update && \
    apt-get install -y nginx procps curl && \
    rm -rf /var/lib/apt/lists/*

# 创建必要的目录
RUN mkdir -p /app/frontend/dist /app/backend /var/log/nginx

# 复制前端构建产物
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 复制后端代码和依赖
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /app/backend /app/backend

# 设置权限
RUN chown -R www-data:www-data /app/frontend/dist && \
    chown -R www-data:www-data /var/log/nginx && \
    chown -R www-data:www-data /app

# 复制启动脚本并设置权限
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# 暴露端口
EXPOSE 8728 8000

# 启动服务
ENTRYPOINT ["/app/docker-entrypoint.sh"] 