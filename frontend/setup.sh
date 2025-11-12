#!/bin/bash

# 前端环境设置脚本

echo "正在设置前端环境..."

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "错误: Node.js未安装，请先安装Node.js"
    exit 1
fi

echo "Node版本: $(node -v)"
echo "npm版本: $(npm -v)"

# 安装依赖
echo "安装依赖..."
npm install

echo ""
echo "前端环境设置完成！"
echo ""
echo "接下来的步骤："
echo "1. 确保后端服务已启动（http://localhost:8000）"
echo "2. 运行开发服务器：npm run dev"
echo "3. 访问 http://localhost:5173"

