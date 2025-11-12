#!/bin/bash

# 后端服务启动脚本

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "错误: 虚拟环境不存在，请先运行 setup.sh"
    exit 1
fi

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "错误: .env文件不存在，请先运行 setup.sh"
    exit 1
fi

echo "启动后端服务..."
python main.py

