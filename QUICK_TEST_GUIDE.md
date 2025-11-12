# 快速测试指南

## 🚀 快速启动测试

### 1. 初始化数据库
```bash
cd /Users/lihui/Work/cursor/claude-mysterious/backend
python init_db.py
```

预期输出：
```
Creating database tables...
Database tables created successfully!
Creating default admin user...
Default admin user created successfully!
Username: admin
Password: admin
Real Name: 系统管理员
```

### 2. 启动系统
```bash
cd /Users/lihui/Work/cursor/claude-mysterious
./start-all.sh
```

### 3. 访问系统
浏览器打开：**http://localhost:1212**

---

## ✅ 测试用例

### 测试一：登录功能
1. 访问 http://localhost:1212
2. 输入用户名：`admin`
3. 输入密码：`admin`
4. 点击"登录"
5. ✅ 应成功登录并跳转到用户管理页面

### 测试二：查看用户列表
1. 登录后自动进入用户管理页面
2. ✅ 应该看到至少一个admin用户
3. ✅ 表格应显示：ID、用户名、真实姓名、生效时间、失效时间、状态、角色
4. ✅ admin用户的角色标签应为"管理员"

### 测试三：新增用户
1. 点击右上角"新增用户"按钮
2. 填写信息：
   - 用户名：`testuser`
   - 密码：`test123`
   - 真实姓名：`测试用户`
3. 点击"确定"
4. ✅ 应提示"创建成功"
5. ✅ 列表中应出现新用户
6. ✅ 新用户的角色标签应为"普通用户"

### 测试四：编辑用户
1. 找到刚创建的testuser
2. 点击"编辑"按钮
3. 修改真实姓名为：`测试用户-已修改`
4. 修改密码：`newpass123`
5. 点击"确定"
6. ✅ 应提示"更新成功"
7. ✅ 真实姓名应已更新

### 测试五：搜索用户
1. 在搜索框输入：`test`
2. 点击搜索图标
3. ✅ 应只显示包含"test"的用户
4. 点击清空
5. ✅ 应显示所有用户

### 测试六：删除用户
1. 找到testuser
2. 点击"删除"按钮
3. 确认删除
4. ✅ 应提示"删除成功"
5. ✅ 列表中不应再有该用户
6. 尝试删除admin用户
7. ✅ 删除按钮应该是禁用状态

### 测试七：配置管理-查看列表
1. 点击左侧菜单"配置管理"
2. ✅ 应进入配置管理页面
3. ✅ 页面应显示配置列表（可能为空）

### 测试八：新增配置
1. 点击"新增配置"按钮
2. 填写信息：
   - 配置字段：`app.name`
   - 字段值：`Mysterious压测平台`
   - 描述：`应用名称`
3. 点击"确定"
4. ✅ 应提示"创建成功"
5. ✅ 列表中应出现新配置
6. ✅ 创建人应显示为"admin"

### 测试九：编辑配置
1. 找到刚创建的配置
2. 点击"编辑"按钮
3. ✅ 配置字段应该是禁用状态（不可编辑）
4. 修改字段值为：`Mysterious压测平台 v1.0`
5. 修改描述为：`应用名称和版本`
6. 点击"确定"
7. ✅ 应提示"更新成功"
8. ✅ 修改人应更新为"admin"
9. ✅ 修改时间应更新

### 测试十：配置搜索
1. 创建多个配置：
   - `app.version` / `1.0.0` / `应用版本`
   - `db.host` / `localhost` / `数据库地址`
   - `db.port` / `3306` / `数据库端口`
2. 在搜索框输入：`db`
3. 点击搜索
4. ✅ 应只显示配置字段包含"db"的配置
5. 清空搜索
6. ✅ 应显示所有配置

### 测试十一：删除配置
1. 找到一个配置
2. 点击"删除"按钮
3. 确认删除
4. ✅ 应提示"删除成功"
5. ✅ 列表中不应再有该配置

### 测试十二：分页测试
1. 创建超过10个用户或配置
2. ✅ 应该显示分页控件
3. 切换到第2页
4. ✅ 应该显示不同的数据
5. 修改每页显示数量为20
6. ✅ 应该显示更多数据

### 测试十三：权限测试（需要第二个测试用户）
1. 创建一个普通用户testuser2
2. 退出登录
3. 使用testuser2登录
4. ✅ 应该能查看用户列表和配置列表
5. ✅ "新增用户"按钮应该不显示
6. ✅ "新增配置"按钮应该不显示
7. ✅ 操作列的"编辑"和"删除"按钮应该不显示

### 测试十四：账号过期测试
1. 登录admin
2. 创建一个用户，然后直接在数据库修改其expire_time为过去的时间
3. 使用该用户登录
4. ✅ 应提示"User account expired"

### 测试十五：API文档测试
1. 访问 http://localhost:2121/docs
2. ✅ 应该看到Swagger API文档
3. ✅ 应该包含用户管理和配置管理的所有端点
4. 测试登录接口：
   - 点击 POST /api/auth/login
   - 点击 "Try it out"
   - 输入：`{"username": "admin", "password": "admin"}`
   - 点击 Execute
   - ✅ 应返回access_token

---

## 📊 数据库验证

### 查看用户表
```sql
USE claude_mysterious;
SELECT * FROM mysterious_user;
```

预期结果：
```
+----+----------+----------+--------------+-------+---------------------+---------------------+
| id | username | password | real_name    | token | effect_time         | expire_time         |
+----+----------+----------+--------------+-------+---------------------+---------------------+
|  1 | admin    | $2b$...  | 系统管理员    | ...   | 2024-11-12 10:00:00 | 2124-11-12 10:00:00 |
+----+----------+----------+--------------+-------+---------------------+---------------------+
```

### 查看配置表
```sql
SELECT * FROM mysterious_config;
```

预期结果：
```
+----+--------------+---------------------+--------------+------------+---------+-------------+----------+---------------------+---------------------+
| id | config_key   | config_value        | description  | creator_id | creator | modifier_id | modifier | create_time         | modify_time         |
+----+--------------+---------------------+--------------+------------+---------+-------------+----------+---------------------+---------------------+
|  1 | app.name     | Mysterious压测平台   | 应用名称      | 1          | admin   | 1           | admin    | 2024-11-12 10:00:00 | 2024-11-12 10:00:00 |
+----+--------------+---------------------+--------------+------------+---------+-------------+----------+---------------------+---------------------+
```

---

## 🐛 常见问题排查

### 问题1：数据库连接失败
```bash
# 检查MySQL是否运行
ps aux | grep mysql

# 检查数据库是否存在
mysql -u root -pTest@123456 -e "SHOW DATABASES LIKE 'claude_mysterious';"

# 如果不存在，创建数据库
mysql -u root -pTest@123456 -e "CREATE DATABASE claude_mysterious CHARACTER SET utf8mb4;"
```

### 问题2：表不存在
```bash
# 重新初始化数据库
cd backend
source venv/bin/activate
python init_db.py
```

### 问题3：登录失败
- 确认用户名是：admin（小写）
- 确认密码是：admin（小写）
- 检查后端日志是否有错误

### 问题4：前端无法访问后端
- 确认后端运行在端口2121
- 确认前端运行在端口1212
- 检查浏览器控制台Network标签

### 问题5：权限不足
- 确认使用admin用户登录
- 检查token是否有效
- 查看响应错误信息

---

## 📈 性能测试

### 测试大量数据
```python
# 创建测试脚本 test_bulk_insert.py
from backend.database import SessionLocal
from backend.models import Config
from datetime import datetime

db = SessionLocal()

# 批量创建100个配置
for i in range(100):
    config = Config(
        config_key=f"test.config.{i}",
        config_value=f"value_{i}",
        description=f"测试配置{i}",
        creator_id="1",
        creator="admin",
        modifier_id="1",
        modifier="admin",
        create_time=datetime.now(),
        modify_time=datetime.now()
    )
    db.add(config)

db.commit()
print("Created 100 test configs")
```

运行后测试分页功能。

---

## ✅ 测试完成清单

- [ ] 登录功能正常
- [ ] 查看用户列表正常
- [ ] 新增用户功能正常
- [ ] 编辑用户功能正常
- [ ] 删除用户功能正常
- [ ] 搜索用户功能正常
- [ ] 查看配置列表正常
- [ ] 新增配置功能正常
- [ ] 编辑配置功能正常
- [ ] 删除配置功能正常
- [ ] 搜索配置功能正常
- [ ] 分页功能正常
- [ ] 权限控制正常
- [ ] 创建人/修改人记录正常
- [ ] API文档可访问

---

**测试愉快！** 🎉

