# 构建阶段
FROM node:18-alpine as frontend-builder

WORKDIR /app/frontend
COPY frontend/graylink-web/package*.json ./
RUN npm install

COPY frontend/graylink-web ./
RUN npm run build

# 后端构建阶段
FROM python:3.11-slim as backend-builder

WORKDIR /app/backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./

# 生产阶段
FROM nginx:alpine

# 复制前端构建产物
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html

# 复制后端代码
COPY --from=backend-builder /app/backend /app/backend

# 复制 nginx 配置
COPY frontend/graylink-web/nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动命令
CMD ["nginx", "-g", "daemon off;"] 