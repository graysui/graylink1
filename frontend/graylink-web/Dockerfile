# 构建阶段
FROM node:20-alpine as build-stage

WORKDIR /app

# 设置 npm 配置
RUN npm config set registry https://registry.npmmirror.com/ && \
    npm config set legacy-peer-deps true

# 先复制 package.json 和 package-lock.json
COPY package*.json ./

# 安装所有依赖
RUN npm install --legacy-peer-deps

# 复制其余源代码
COPY . .

# 构建前检查目录结构
RUN ls -la && \
    # 构建
    npm run build-only && \
    # 检查构建产物
    ls -la dist/

# 生产阶段
FROM nginx:alpine as production-stage

# 创建必要的目录
RUN mkdir -p /usr/share/nginx/html

# 复制构建产物前检查源目录
COPY --from=build-stage /app/dist/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 检查文件是否正确复制
RUN ls -la /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 