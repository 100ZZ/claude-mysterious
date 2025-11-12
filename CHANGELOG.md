# 更新日志

## [1.1.0] - 2024-11-12

### 新增功能
- ✨ 添加配置管理功能
  - 支持配置的增删改查
  - 支持按配置字段搜索
  - 支持分页查询
  - 仅管理员可以操作配置

### 变更
- 🔧 修改后端端口：8000 → 2121
- 🔧 修改前端端口：5173 → 1212
- 📝 更新相关文档和配置

### 新增文件
- `backend/models.py` - 添加Config数据模型
- `backend/schemas.py` - 添加Config相关Schema
- `backend/crud_config.py` - 配置管理CRUD操作
- `frontend/src/types/config.ts` - 配置类型定义
- `frontend/src/api/config.ts` - 配置API接口
- `frontend/src/views/Configs.vue` - 配置管理页面

### 数据库变更
- 新增表：`configs`
  - id: 主键
  - config_key: 配置字段（唯一）
  - config_value: 字段值
  - description: 描述
  - created_at: 创建时间
  - updated_at: 更新时间

---

## [1.0.0] - 2024-11-12

### 初始版本
- 🎉 用户管理系统完整实现
- 🔐 JWT认证
- 👥 用户增删改查
- 🛡️ 权限控制
- 📱 响应式前端界面
- 📖 完整文档

