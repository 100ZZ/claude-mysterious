# Claude Mysterious Backend

基于 FastAPI + MySQL 8.0 的后端服务

## 环境要求

- Python 3.8+
- MySQL 8.0
- pip

## 安装步骤

1. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# 或 venv\Scripts\activate  # Windows
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
复制 `.env` 文件并根据实际情况修改数据库连接信息

4. 创建数据库
```bash
mysql -u root -p
CREATE DATABASE claude_mysterious CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

5. 初始化数据库
```bash
python init_db.py
```

6. 运行服务
```bash
python main.py
# 或者
uvicorn main:app --reload --port 8000
```

## API文档

启动服务后访问: http://localhost:8000/docs

## 默认用户

- 用户名: admin
- 密码: admin

## API端点

### 认证
- POST `/api/auth/login` - 用户登录
- GET `/api/auth/me` - 获取当前用户信息

### 用户管理（需要admin权限）
- GET `/api/users` - 获取用户列表
- GET `/api/users/{user_id}` - 获取用户详情
- POST `/api/users` - 创建用户
- PUT `/api/users/{user_id}` - 更新用户
- DELETE `/api/users/{user_id}` - 删除用户

