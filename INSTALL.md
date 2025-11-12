# 安装指南

## 方式一：使用一键启动脚本（推荐）

### 前提条件

1. 已安装 Python 3.8+
2. 已安装 Node.js 16+
3. 已安装 MySQL 8.0 并启动服务
4. 已创建数据库 `claude_mysterious`

### 创建数据库

```bash
mysql -u root -p
# 输入密码：Test@123456

CREATE DATABASE claude_mysterious CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

### 一键启动

```bash
# 给脚本添加执行权限
chmod +x start-all.sh
chmod +x backend/setup.sh
chmod +x backend/run.sh
chmod +x frontend/setup.sh

# 运行启动脚本
./start-all.sh
```

脚本会自动完成：
- 创建Python虚拟环境
- 安装后端依赖
- 创建.env配置文件
- 初始化数据库和创建默认管理员
- 安装前端依赖
- 启动后端和前端服务

启动成功后：
- 前端地址：http://localhost:5173
- 后端地址：http://localhost:8000
- API文档：http://localhost:8000/docs

---

## 方式二：手动分步安装

### 步骤1：创建数据库

```bash
mysql -u root -p
# 输入密码：Test@123456

CREATE DATABASE claude_mysterious CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

### 步骤2：后端设置

```bash
cd backend

# 方式A：使用脚本（推荐）
chmod +x setup.sh
./setup.sh

# 方式B：手动设置
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 创建.env文件
cat > .env << EOF
DATABASE_URL=mysql+pymysql://root:Test@123456@localhost:3306/claude_mysterious
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF

# 初始化数据库
python init_db.py

# 启动后端服务
python main.py
```

### 步骤3：前端设置

打开新终端：

```bash
cd frontend

# 方式A：使用脚本（推荐）
chmod +x setup.sh
./setup.sh
npm run dev

# 方式B：手动设置
npm install
npm run dev
```

---

## Windows用户安装步骤

### 1. 创建数据库
同上

### 2. 后端设置

```cmd
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 手动创建.env文件，内容如下：
# DATABASE_URL=mysql+pymysql://root:Test@123456@localhost:3306/claude_mysterious
# SECRET_KEY=your-secret-key-change-this-in-production
# ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES=30

# 初始化数据库
python init_db.py

# 启动后端
python main.py
```

### 3. 前端设置

打开新的命令行窗口：

```cmd
cd frontend

# 安装依赖
npm install

# 启动前端
npm run dev
```

---

## 验证安装

1. 访问前端：http://localhost:5173
2. 使用默认账号登录：
   - 用户名：`admin`
   - 密码：`admin`
3. 登录成功后应该能看到用户管理界面

---

## 常见问题

### 1. 数据库连接失败

**错误信息**：`Can't connect to MySQL server`

**解决方案**：
- 确认MySQL服务已启动
- 检查数据库用户名和密码是否正确
- 确认数据库`claude_mysterious`已创建
- 检查MySQL端口是否为3306

### 2. Python依赖安装失败

**错误信息**：`error: Microsoft Visual C++ 14.0 or greater is required`

**解决方案**（Windows）：
- 下载并安装 Microsoft C++ Build Tools
- 或使用预编译的wheel包：`pip install --only-binary :all: cryptography`

### 3. 前端依赖安装失败

**错误信息**：`npm ERR! code ELIFECYCLE`

**解决方案**：
```bash
# 清除npm缓存
npm cache clean --force

# 删除node_modules
rm -rf node_modules package-lock.json

# 重新安装
npm install
```

### 4. 端口被占用

**错误信息**：`Address already in use`

**解决方案**：
```bash
# 查找占用8000端口的进程（后端）
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# 查找占用5173端口的进程（前端）
lsof -i :5173  # Mac/Linux
netstat -ano | findstr :5173  # Windows

# 杀死进程或修改配置文件中的端口
```

### 5. .env文件创建问题

如果无法创建.env文件，可以手动创建：

**backend/.env**:
```
DATABASE_URL=mysql+pymysql://root:Test@123456@localhost:3306/claude_mysterious
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 停止服务

### 使用一键启动脚本启动的
按 `Ctrl+C` 停止所有服务

### 手动启动的
在各自的终端窗口按 `Ctrl+C`

---

## 下一步

安装完成后，请阅读 [README.md](./README.md) 了解更多功能和使用说明。

