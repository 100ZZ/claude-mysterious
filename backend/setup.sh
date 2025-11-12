#!/bin/bash

# 后端环境设置脚本

echo "正在设置后端环境..."

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 创建.env文件（如果不存在）
if [ ! -f ".env" ]; then
    echo "创建.env配置文件..."
    cat > .env << EOF
DATABASE_URL=mysql+pymysql://root:Test@123456@localhost:3306/claude_mysterious
SECRET_KEY=your-secret-key-change-this-in-production-$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF
    echo ".env文件已创建"
else
    echo ".env文件已存在，跳过创建"
fi

echo ""
echo "后端环境设置完成！"
echo ""
echo "接下来的步骤："
echo "1. 确保MySQL服务正在运行"
echo "2. 确保已创建数据库：CREATE DATABASE claude_mysterious;"
echo "3. 运行数据库初始化：python init_db.py"
echo "4. 启动后端服务：python main.py"

