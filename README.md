# Claude Mysterious - 用户管理系统

一个基于 Vue3 + TypeScript + FastAPI + MySQL 8.0 的前后端分离用户管理系统。

## 系统架构

- **前端**: Vue3 + TypeScript + Element Plus + Pinia + Vue Router
- **后端**: FastAPI + SQLAlchemy + PyMySQL
- **数据库**: MySQL 8.0

## 功能特性

- ✅ 用户登录认证（JWT Token）
- ✅ 用户管理（增删改查）
- ✅ 配置管理（增删改查，支持搜索）
- ✅ 权限控制（只有管理员可以新增/删除/更新用户和配置）
- ✅ 默认管理员账号：admin/admin
- ✅ 响应式设计
- ✅ CORS跨域支持
- ✅ 分页查询

## 快速开始

### 前置要求

- Python 3.8+
- Node.js 16+
- MySQL 8.0
- npm 或 yarn

### 1. 数据库设置

```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE claude_mysterious CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 退出
exit;
```

### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Mac/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 创建 .env 文件（根据 .env.example）
cat > .env << EOF
DATABASE_URL=mysql+pymysql://root:Test@123456@localhost:3306/claude_mysterious
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF

# 初始化数据库（创建表和默认管理员用户）
python init_db.py

# 运行后端服务
python main.py
```

后端服务将运行在: http://localhost:2121

API文档: http://localhost:2121/docs

### 3. 前端设置

```bash
# 打开新终端，进入前端目录
cd frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev
```

前端服务将运行在: http://localhost:1212

## 默认账号

- **用户名**: admin
- **密码**: admin
- **权限**: 管理员（可以增删改查用户）

## API端点

### 认证相关

- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息

### 用户管理（需要认证）

- `GET /api/users` - 获取用户列表
- `GET /api/users/{user_id}` - 获取用户详情
- `POST /api/users` - 创建用户（需要管理员权限）
- `PUT /api/users/{user_id}` - 更新用户（需要管理员权限）
- `DELETE /api/users/{user_id}` - 删除用户（需要管理员权限）

### 配置管理（需要认证）

- `GET /api/configs` - 获取配置列表（支持分页和搜索）
- `GET /api/configs/{config_id}` - 获取配置详情
- `POST /api/configs` - 创建配置（需要管理员权限）
- `PUT /api/configs/{config_id}` - 更新配置（需要管理员权限）
- `DELETE /api/configs/{config_id}` - 删除配置（需要管理员权限）

## 项目结构

```
claude-mysterious/
├── backend/                # 后端项目
│   ├── main.py            # 主应用入口
│   ├── config.py          # 配置文件
│   ├── database.py        # 数据库连接
│   ├── models.py          # 数据模型
│   ├── schemas.py         # Pydantic模型
│   ├── auth.py            # 认证相关
│   ├── crud.py            # 数据库操作
│   ├── init_db.py         # 数据库初始化脚本
│   ├── requirements.txt   # Python依赖
│   └── README.md          # 后端说明文档
│
├── frontend/              # 前端项目
│   ├── src/
│   │   ├── api/          # API接口
│   │   ├── router/       # 路由配置
│   │   ├── stores/       # 状态管理
│   │   ├── types/        # TypeScript类型
│   │   ├── views/        # 页面组件
│   │   ├── App.vue       # 根组件
│   │   └── main.ts       # 入口文件
│   ├── package.json      # npm依赖
│   ├── vite.config.ts    # Vite配置
│   └── README.md         # 前端说明文档
│
└── README.md             # 项目总说明（本文件）
```

## 开发说明

### 数据库配置

数据库连接信息配置在 `backend/.env` 文件中：

```
DATABASE_URL=mysql+pymysql://root:Test@123456@localhost:3306/claude_mysterious
```

如需修改，请更新此文件。

### 安全性说明

- JWT Token 用于用户认证
- 密码使用 bcrypt 加密存储
- CORS 配置在 `backend/main.py` 中
- 生产环境请务必修改 `SECRET_KEY`

### 权限控制

- 普通用户：可以查看用户列表
- 管理员用户：可以新增、编辑、删除用户
- 用户不能删除自己

## 故障排查

### 后端问题

1. **数据库连接失败**
   - 检查 MySQL 服务是否运行
   - 确认数据库用户名和密码正确
   - 确认数据库 `claude_mysterious` 已创建

2. **依赖安装失败**
   - 确保 Python 版本 >= 3.8
   - 尝试升级 pip: `pip install --upgrade pip`

### 前端问题

1. **依赖安装失败**
   - 确保 Node.js 版本 >= 16
   - 尝试清除缓存: `npm cache clean --force`
   - 删除 `node_modules` 后重新安装

2. **API请求失败**
   - 确保后端服务已启动
   - 检查浏览器控制台的网络请求

## 生产部署建议

1. **后端**
   - 使用 Gunicorn 或 Uvicorn 部署
   - 配置反向代理（Nginx）
   - 使用环境变量管理敏感配置
   - 启用 HTTPS

2. **前端**
   - 执行 `npm run build` 构建生产版本
   - 部署 `dist` 目录到静态服务器
   - 配置 Nginx 反向代理

3. **数据库**
   - 定期备份
   - 配置访问权限
   - 使用强密码

## 技术栈详细说明

### 后端技术

- **FastAPI**: 现代、快速的 Python Web 框架
- **SQLAlchemy**: Python SQL 工具包和 ORM
- **PyMySQL**: MySQL 数据库连接器
- **python-jose**: JWT Token 处理
- **passlib**: 密码加密
- **Pydantic**: 数据验证

### 前端技术

- **Vue 3**: 渐进式 JavaScript 框架
- **TypeScript**: JavaScript 的超集
- **Element Plus**: Vue 3 UI 组件库
- **Pinia**: Vue 状态管理
- **Vue Router**: Vue 路由管理
- **Axios**: HTTP 客户端
- **Vite**: 下一代前端构建工具

## 许可证

MIT License

## 联系方式

如有问题，请提交 Issue。

