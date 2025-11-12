#!/bin/bash

# 一键启动前后端服务

echo "======================================"
echo "  Claude Mysterious 系统启动脚本"
echo "======================================"
echo ""

# 检查MySQL
echo "检查MySQL服务..."
if ! pgrep -x "mysqld" > /dev/null; then
    echo "警告: MySQL服务未运行，请先启动MySQL"
    exit 1
fi
echo "✓ MySQL服务正在运行"
echo ""

# 启动后端
echo "启动后端服务..."
cd backend
if [ ! -d "venv" ]; then
    echo "后端虚拟环境不存在，正在创建..."
    ./setup.sh
fi

# 检查数据库是否初始化
if [ ! -f ".db_initialized" ]; then
    echo "初始化数据库..."
    source venv/bin/activate
    python init_db.py
    touch .db_initialized
    deactivate
fi

source venv/bin/activate
echo "后端服务启动在 http://localhost:2121"
python main.py &
BACKEND_PID=$!
deactivate
cd ..

# 等待后端启动
echo "等待后端服务启动..."
sleep 3

# 启动前端
echo "启动前端服务..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi
echo "前端服务启动在 http://localhost:1212"
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "======================================"
echo "  系统启动成功！"
echo "======================================"
echo ""
echo "前端地址: http://localhost:1212"
echo "后端地址: http://localhost:2121"
echo "API文档: http://localhost:2121/docs"
echo ""
echo "默认登录账号："
echo "  用户名: admin"
echo "  密码: admin"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo ""

# 等待用户中断
trap "echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait

