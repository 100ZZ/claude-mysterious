# API 使用示例

本文档提供了常见API调用的示例，方便开发和测试。

## 🔐 认证相关

### 1. 用户登录

**请求**:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin"
  }'
```

**响应**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTYzOTU4ODgwMH0.xxxxx",
  "token_type": "bearer"
}
```

### 2. 获取当前用户信息

**请求**:
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**响应**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "full_name": "Administrator",
  "is_active": true,
  "is_admin": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": null
}
```

---

## 👥 用户管理

### 3. 获取用户列表

**请求**:
```bash
curl -X GET "http://localhost:8000/api/users" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**响应**:
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "full_name": "Administrator",
    "is_active": true,
    "is_admin": true,
    "created_at": "2024-01-01T00:00:00"
  },
  {
    "id": 2,
    "username": "user1",
    "email": "user1@example.com",
    "full_name": "User One",
    "is_active": true,
    "is_admin": false,
    "created_at": "2024-01-02T00:00:00"
  }
]
```

### 4. 获取单个用户

**请求**:
```bash
curl -X GET "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**响应**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "full_name": "Administrator",
  "is_active": true,
  "is_admin": true,
  "created_at": "2024-01-01T00:00:00"
}
```

### 5. 创建新用户（需要管理员权限）

**请求**:
```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE" \
  -d '{
    "username": "newuser",
    "password": "password123",
    "email": "newuser@example.com",
    "full_name": "New User",
    "is_active": true
  }'
```

**响应**:
```json
{
  "id": 3,
  "username": "newuser",
  "email": "newuser@example.com",
  "full_name": "New User",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-03T00:00:00"
}
```

### 6. 更新用户（需要管理员权限）

**请求**:
```bash
curl -X PUT "http://localhost:8000/api/users/3" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE" \
  -d '{
    "email": "updated@example.com",
    "full_name": "Updated Name",
    "is_active": true
  }'
```

**响应**:
```json
{
  "id": 3,
  "username": "newuser",
  "email": "updated@example.com",
  "full_name": "Updated Name",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-03T00:00:00",
  "updated_at": "2024-01-03T10:00:00"
}
```

### 7. 修改用户密码（需要管理员权限）

**请求**:
```bash
curl -X PUT "http://localhost:8000/api/users/3" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE" \
  -d '{
    "password": "newpassword123"
  }'
```

### 8. 删除用户（需要管理员权限）

**请求**:
```bash
curl -X DELETE "http://localhost:8000/api/users/3" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE"
```

**响应**:
```json
{
  "message": "User deleted successfully"
}
```

---

## 🔒 权限说明

### 普通用户权限
- ✅ 登录
- ✅ 查看自己的信息
- ✅ 查看用户列表
- ✅ 查看单个用户详情
- ❌ 创建用户
- ❌ 更新用户
- ❌ 删除用户

### 管理员权限
- ✅ 所有普通用户权限
- ✅ 创建新用户
- ✅ 更新用户信息
- ✅ 删除用户（不能删除自己）
- ✅ 修改用户密码

---

## 📝 JavaScript/TypeScript 示例

### 使用 Axios

```typescript
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

// 创建axios实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000
})

// 登录
async function login(username: string, password: string) {
  const response = await api.post('/auth/login', {
    username,
    password
  })
  const { access_token } = response.data
  localStorage.setItem('token', access_token)
  return access_token
}

// 获取用户列表
async function getUsers() {
  const token = localStorage.getItem('token')
  const response = await api.get('/users', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  return response.data
}

// 创建用户
async function createUser(userData: {
  username: string
  password: string
  email?: string
  full_name?: string
}) {
  const token = localStorage.getItem('token')
  const response = await api.post('/users', userData, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  return response.data
}

// 更新用户
async function updateUser(userId: number, userData: {
  email?: string
  full_name?: string
  is_active?: boolean
  password?: string
}) {
  const token = localStorage.getItem('token')
  const response = await api.put(`/users/${userId}`, userData, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  return response.data
}

// 删除用户
async function deleteUser(userId: number) {
  const token = localStorage.getItem('token')
  await api.delete(`/users/${userId}`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
}
```

---

## 🐍 Python 示例

### 使用 requests

```python
import requests

API_BASE_URL = 'http://localhost:8000/api'

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.token = None
    
    def login(self, username: str, password: str):
        """用户登录"""
        response = requests.post(
            f'{self.base_url}/auth/login',
            json={'username': username, 'password': password}
        )
        response.raise_for_status()
        data = response.json()
        self.token = data['access_token']
        return self.token
    
    def _get_headers(self):
        """获取请求头"""
        if not self.token:
            raise Exception('Not authenticated')
        return {'Authorization': f'Bearer {self.token}'}
    
    def get_users(self):
        """获取用户列表"""
        response = requests.get(
            f'{self.base_url}/users',
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def create_user(self, username: str, password: str, **kwargs):
        """创建用户"""
        data = {
            'username': username,
            'password': password,
            **kwargs
        }
        response = requests.post(
            f'{self.base_url}/users',
            json=data,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def update_user(self, user_id: int, **kwargs):
        """更新用户"""
        response = requests.put(
            f'{self.base_url}/users/{user_id}',
            json=kwargs,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def delete_user(self, user_id: int):
        """删除用户"""
        response = requests.delete(
            f'{self.base_url}/users/{user_id}',
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

# 使用示例
if __name__ == '__main__':
    client = APIClient()
    
    # 登录
    client.login('admin', 'admin')
    
    # 获取用户列表
    users = client.get_users()
    print(f'Total users: {len(users)}')
    
    # 创建新用户
    new_user = client.create_user(
        username='testuser',
        password='testpass',
        email='test@example.com',
        full_name='Test User'
    )
    print(f'Created user: {new_user["username"]}')
```

---

## ⚠️ 错误响应

### 401 Unauthorized - 未授权
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden - 无权限
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found - 资源不存在
```json
{
  "detail": "User not found"
}
```

### 400 Bad Request - 请求错误
```json
{
  "detail": "Username already registered"
}
```

---

## 🔍 Swagger UI

访问 http://localhost:8000/docs 可以：
- 查看所有API文档
- 在线测试API
- 查看请求/响应模型
- 生成代码示例

---

## 📚 相关文档

- [README.md](./README.md) - 项目总览
- [QUICKSTART.md](./QUICKSTART.md) - 快速开始
- [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) - 项目结构

---

**提示**: 实际使用时，请替换 `YOUR_TOKEN_HERE` 和 `YOUR_ADMIN_TOKEN_HERE` 为真实的JWT Token。

