# 快速开始指南 ⚡

5分钟内启动并运行 Claude Mysterious 用户管理系统！

## 📋 前提检查

在开始之前，确保你已安装：

- [ ] Python 3.8+ （运行 `python3 --version`）
- [ ] Node.js 16+ （运行 `node -v`）
- [ ] MySQL 8.0 （运行 `mysql --version`）
- [ ] npm （运行 `npm -v`）

## 🚀 三步启动

### 第一步：创建数据库

```bash
# 登录 MySQL
mysql -u root -p
# 输入密码：Test@123456

# 创建数据库
CREATE DATABASE claude_mysterious CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 退出
exit;
```

### 第二步：一键启动

```bash
# 在项目根目录执行
./start-all.sh
```

就这么简单！脚本会自动完成所有设置。

### 第三步：访问系统

浏览器访问：http://localhost:5173

**登录账号**：
- 用户名：`admin`
- 密码：`admin`

---

## 🎯 完成！

现在你可以：

✅ 查看用户列表  
✅ 新增用户（仅管理员）  
✅ 编辑用户信息（仅管理员）  
✅ 删除用户（仅管理员）  
✅ 查看用户详情

---

## 🔗 重要链接

- **前端界面**：http://localhost:5173
- **后端API**：http://localhost:8000
- **API文档**：http://localhost:8000/docs（Swagger UI）
- **详细文档**：查看 [README.md](./README.md)
- **安装指南**：查看 [INSTALL.md](./INSTALL.md)

---

## 🛠️ 手动启动（可选）

如果你想分步启动：

### 启动后端

```bash
cd backend
chmod +x setup.sh run.sh
./setup.sh    # 首次运行
./run.sh      # 启动服务
```

### 启动前端（新终端）

```bash
cd frontend
chmod +x setup.sh
./setup.sh    # 首次运行
npm run dev   # 启动服务
```

---

## 📱 快速测试API

使用 curl 测试登录：

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

应该返回类似：

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## ❓ 遇到问题？

### 常见问题快速修复

**问题1：数据库连接失败**
```bash
# 检查MySQL是否运行
ps aux | grep mysql  # Mac/Linux
tasklist | findstr mysql  # Windows

# 启动MySQL
brew services start mysql  # Mac
sudo service mysql start  # Linux
net start MySQL80  # Windows
```

**问题2：端口被占用**
```bash
# 查看占用端口的进程
lsof -i :8000  # 后端端口
lsof -i :5173  # 前端端口

# 或者修改端口：
# 后端：修改 backend/main.py 最后一行的 port 参数
# 前端：修改 frontend/vite.config.ts 中的 server.port
```

**问题3：Python虚拟环境问题**
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**更多问题**：查看 [INSTALL.md](./INSTALL.md) 的常见问题部分

---

## 🎓 下一步学习

1. 📖 阅读完整的 [README.md](./README.md)
2. 🔍 探索 [API文档](http://localhost:8000/docs)
3. 💻 查看源代码了解实现细节
4. 🚀 根据需求定制功能

---

## 🛑 停止服务

按 `Ctrl+C` 停止所有服务

---

## 📞 需要帮助？

如果遇到任何问题：

1. 查看 [INSTALL.md](./INSTALL.md) 的故障排查部分
2. 检查终端的错误信息
3. 提交 Issue 描述你的问题

---

**祝使用愉快！** 🎉

