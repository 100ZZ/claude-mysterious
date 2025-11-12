# 数据库表结构更新总结

## 📋 更新时间
2024-11-12

## 🎯 更新目标
根据提供的MySQL表结构，将系统从简单的用户管理系统更新为符合mysterious_user和mysterious_config表结构的压测平台用户&配置管理模块。

---

## 📊 表结构变更

### 1. 用户表变更

#### 旧表结构 (users)
```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50),
    hashed_password VARCHAR(255),
    email VARCHAR(100),
    full_name VARCHAR(100),
    is_active BOOLEAN,
    is_admin BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
```

#### 新表结构 (mysterious_user)
```sql
CREATE TABLE mysterious_user (
    id BIGINT(20) PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(128) NOT NULL DEFAULT '',
    password VARCHAR(128) NOT NULL DEFAULT '',
    real_name VARCHAR(128) NOT NULL DEFAULT '',
    token VARCHAR(128) NOT NULL DEFAULT '',
    effect_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expire_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
)
```

#### 主要变更
- ✅ 表名：`users` → `mysterious_user`
- ✅ ID类型：`INT` → `BIGINT(20)`
- ✅ 密码字段：`hashed_password` → `password`
- ✅ 真实姓名：`full_name` → `real_name`
- ✅ **新增**：`token` 字段（用于存储JWT token）
- ✅ **新增**：`effect_time` 字段（生效时间）
- ✅ **新增**：`expire_time` 字段（失效时间）
- ❌ **删除**：`email`、`is_active`、`is_admin` 字段
- ❌ **删除**：`created_at`、`updated_at` 时间戳

### 2. 配置表变更

#### 旧表结构 (configs)
```sql
CREATE TABLE configs (
    id INT PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE,
    config_value TEXT,
    description VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
```

#### 新表结构 (mysterious_config)
```sql
CREATE TABLE mysterious_config (
    id BIGINT(20) PRIMARY KEY AUTO_INCREMENT,
    config_key VARCHAR(255) NOT NULL DEFAULT '',
    config_value VARCHAR(255) NOT NULL DEFAULT '',
    description VARCHAR(255) NOT NULL DEFAULT '',
    creator_id VARCHAR(32) NOT NULL DEFAULT '',
    creator VARCHAR(32) NOT NULL DEFAULT '',
    modifier_id VARCHAR(32) NOT NULL DEFAULT '',
    modifier VARCHAR(32) NOT NULL DEFAULT '',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modify_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
)
```

#### 主要变更
- ✅ 表名：`configs` → `mysterious_config`
- ✅ ID类型：`INT` → `BIGINT(20)`
- ✅ config_value类型：`TEXT` → `VARCHAR(255)`
- ✅ **新增**：`creator_id` 字段（创建人ID）
- ✅ **新增**：`creator` 字段（创建人名称）
- ✅ **新增**：`modifier_id` 字段（修改人ID）
- ✅ **新增**：`modifier` 字段（修改人名称）
- ✅ 时间字段：`created_at` → `create_time`
- ✅ 时间字段：`updated_at` → `modify_time`

---

## 💻 后端代码变更

### 1. Models (backend/models.py)
```python
# 更新User模型
class User(Base):
    __tablename__ = "mysterious_user"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(128), nullable=False, default='')
    password = Column(String(128), nullable=False, default='')
    real_name = Column(String(128), nullable=False, default='')
    token = Column(String(128), nullable=False, default='')
    effect_time = Column(DateTime, nullable=False)
    expire_time = Column(DateTime, nullable=False)

# 更新Config模型
class Config(Base):
    __tablename__ = "mysterious_config"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    config_key = Column(String(255), nullable=False, default='')
    config_value = Column(String(255), nullable=False, default='')
    description = Column(String(255), nullable=False, default='')
    creator_id = Column(String(32), nullable=False, default='')
    creator = Column(String(32), nullable=False, default='')
    modifier_id = Column(String(32), nullable=False, default='')
    modifier = Column(String(32), nullable=False, default='')
    create_time = Column(DateTime, nullable=False)
    modify_time = Column(DateTime, nullable=False, onupdate=func.now())
```

### 2. Schemas (backend/schemas.py)
- 更新UserBase、UserCreate、UserUpdate、UserResponse
- 更新ConfigBase、ConfigCreate、ConfigUpdate、ConfigResponse
- 移除email相关字段
- 添加real_name、creator、modifier等字段

### 3. CRUD操作 (backend/crud.py, crud_config.py)
- 更新用户创建逻辑，设置默认生效期和失效期（1年）
- 更新配置CRUD，记录创建人和修改人信息
- 添加分页查询和搜索功能

### 4. 认证逻辑 (backend/auth.py)
```python
# 新增管理员判断函数
def is_admin(user: User) -> bool:
    return user.username == "admin"

# 更新用户验证逻辑
def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.expire_time < datetime.now():
        raise HTTPException(status_code=400, detail="Token expired")
    return current_user

# 更新管理员验证逻辑
def get_admin_user(current_user: User = Depends(get_current_active_user)):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
```

### 5. API端点 (backend/main.py)
- 更新用户列表API，支持分页和搜索
- 更新配置管理API，记录创建人/修改人信息
- 修改密码字段访问：`user.hashed_password` → `user.password`
- 添加token更新逻辑

### 6. 数据库初始化 (backend/init_db.py)
```python
# 更新默认admin用户创建逻辑
admin = User(
    username="admin",
    password=get_password_hash("admin"),
    real_name="系统管理员",
    token="",
    effect_time=datetime.now(),
    expire_time=datetime.now() + timedelta(days=36500)  # 100年
)
```

---

## 🎨 前端代码变更

### 1. 类型定义 (frontend/src/types/)

#### index.ts
```typescript
export interface User {
  id: number
  username: string
  real_name: string
  effect_time: string
  expire_time: string
}

export interface UserCreate {
  username: string
  password: string
  real_name?: string
}

export interface UserUpdate {
  real_name?: string
  password?: string
}

export interface UserListResponse {
  list: User[]
  page: number
  size: number
  total: number
}
```

#### config.ts
```typescript
export interface Config {
  id: number
  config_key: string
  config_value: string
  description: string
  creator_id: string
  creator: string
  modifier_id: string
  modifier: string
  create_time: string
  modify_time: string
}
```

### 2. API接口 (frontend/src/api/)

#### user.ts
- 更新getUsers方法，添加分页参数
- 移除email相关参数

#### config.ts
- ConfigUpdate中移除config_key字段（不允许修改）

### 3. 状态管理 (frontend/src/stores/user.ts)
```typescript
const isAdmin = () => {
  return user.value?.username === 'admin'
}
```

### 4. 用户管理页面 (frontend/src/views/Users.vue)

**新增功能**：
- ✅ 用户名搜索
- ✅ 分页查询（10/20/50/100条每页）
- ✅ 显示生效时间和失效时间
- ✅ 账号过期状态标识
- ✅ 角色标签（管理员/普通用户）

**表格列变更**：
- ID
- 用户名
- 真实姓名（新）
- 生效时间（新）
- 失效时间（新）
- 状态（新：正常/已过期）
- 角色（管理员/普通用户）
- 操作

**表单字段变更**：
- 用户名
- 密码
- 真实姓名（新）

### 5. 配置管理页面 (frontend/src/views/Configs.vue)

**表格列新增**：
- 创建人
- 创建时间
- 修改人
- 修改时间

**其他变更**：
- 配置字段在编辑时不可修改
- 添加字段长度限制（255字符）

---

## 🗄️ 数据库迁移

### 迁移步骤

1. **删除旧表**（如果存在）：
```sql
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS configs;
```

2. **创建新表**：
```bash
cd backend
source venv/bin/activate
python init_db.py
```

3. **初始化admin用户**：
   - 用户名：admin
   - 密码：admin
   - 真实姓名：系统管理员
   - 有效期：100年

---

## ⚙️ 权限控制说明

### 管理员判断逻辑
- **后端**：通过用户名判断（`username == "admin"`）
- **前端**：通过用户名判断（`user.username === 'admin'`）

### 权限限制
- **普通用户**：
  - ✅ 查看用户列表
  - ✅ 查看配置列表
  - ❌ 新增/编辑/删除用户
  - ❌ 新增/编辑/删除配置

- **管理员用户**（admin）：
  - ✅ 所有普通用户权限
  - ✅ 新增/编辑/删除用户
  - ✅ 新增/编辑/删除配置
  - ❌ 删除自己

---

## 🚀 启动说明

### 首次启动

1. **初始化数据库**：
```bash
cd backend
source venv/bin/activate
python init_db.py
```

2. **启动后端**：
```bash
python main.py
# 运行在 http://localhost:2121
```

3. **启动前端**：
```bash
cd frontend
npm run dev
# 运行在 http://localhost:1212
```

### 一键启动
```bash
./start-all.sh
```

---

## 🔐 默认登录信息

- **用户名**：admin
- **密码**：admin
- **角色**：系统管理员
- **有效期**：100年

---

## ✅ 功能验证清单

### 用户管理
- [x] 查看用户列表（分页）
- [x] 搜索用户（按用户名）
- [x] 新增用户（管理员）
- [x] 编辑用户（管理员）
- [x] 删除用户（管理员）
- [x] 显示生效/失效时间
- [x] 显示账号状态
- [x] 显示角色标签

### 配置管理
- [x] 查看配置列表（分页）
- [x] 搜索配置（按配置字段/描述）
- [x] 新增配置（管理员）
- [x] 编辑配置（管理员）
- [x] 删除配置（管理员）
- [x] 显示创建人/时间
- [x] 显示修改人/时间
- [x] 配置字段唯一性验证

### 权限控制
- [x] 管理员判断（username === 'admin'）
- [x] 操作按钮权限控制
- [x] API接口权限验证
- [x] 账号过期检查

---

## 📊 数据示例

### 用户数据示例
```json
{
  "id": 1,
  "username": "admin",
  "real_name": "系统管理员",
  "effect_time": "2024-11-12 10:00:00",
  "expire_time": "2124-11-12 10:00:00"
}
```

### 配置数据示例
```json
{
  "id": 1,
  "config_key": "app.name",
  "config_value": "Mysterious压测平台",
  "description": "应用名称",
  "creator_id": "1",
  "creator": "admin",
  "modifier_id": "1",
  "modifier": "admin",
  "create_time": "2024-11-12 10:00:00",
  "modify_time": "2024-11-12 10:00:00"
}
```

---

## 🎯 下一步建议

根据您提供的完整表结构，系统还可以扩展以下模块：

1. **节点管理** (mysterious_node)
2. **用例管理** (mysterious_testcase)
3. **JMX脚本管理** (mysterious_jmx)
4. **JAR包管理** (mysterious_jar)
5. **CSV文件管理** (mysterious_csv)
6. **报告管理** (mysterious_report)

这些模块的实现可以参考用户和配置管理的模式。

---

## ⚠️ 注意事项

1. **数据迁移**：如果已有旧数据，需要编写迁移脚本
2. **密码字段**：使用bcrypt加密存储
3. **token字段**：每次登录时更新
4. **时间字段**：使用datetime类型，自动维护
5. **配置字段唯一性**：config_key必须唯一
6. **账号有效期**：登录时检查expire_time

---

**更新完成！** ✅

系统已成功更新为符合mysterious数据库表结构的用户和配置管理模块！

