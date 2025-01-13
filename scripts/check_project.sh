#!/bin/bash

echo "开始项目检查..."

# 前端检查
echo "检查前端项目..."
cd frontend/graylink-web
npm ci
npm run type-check
npm run lint
npm run build
npm audit

# 后端检查
echo "检查后端项目..."
cd ../../backend
pip install -r requirements.txt
flake8 .
mypy .
pip check
pytest

# Docker 检查
echo "检查 Docker 配置..."
cd ..
docker run --rm -i hadolint/hadolint < Dockerfile
docker build -t graylink:test .
docker run --rm graylink:test pytest

# 安全检查
echo "执行安全检查..."
safety check
docker scan graylink:test

echo "检查完成！" 