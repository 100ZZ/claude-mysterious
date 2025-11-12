# Claude Mysterious Frontend

基于 Vue3 + TypeScript + Element Plus 的前端应用

## 技术栈

- Vue 3
- TypeScript
- Vue Router
- Pinia (状态管理)
- Element Plus (UI组件库)
- Axios (HTTP客户端)
- Vite (构建工具)

## 安装步骤

1. 安装依赖
```bash
npm install
```

2. 运行开发服务器
```bash
npm run dev
```

3. 构建生产版本
```bash
npm run build
```

4. 预览生产构建
```bash
npm run preview
```

## 功能特性

- 用户登录
- 用户管理（增删改查）
- 权限控制（仅管理员可以增删改用户）
- JWT认证
- 响应式设计

## 默认登录

- 用户名: admin
- 密码: admin

## 目录结构

```
src/
├── api/           # API接口
├── assets/        # 静态资源
├── router/        # 路由配置
├── stores/        # 状态管理
├── types/         # TypeScript类型定义
├── views/         # 页面组件
├── App.vue        # 根组件
└── main.ts        # 入口文件
```

## 开发说明

前端开发服务器运行在 http://localhost:5173

后端API代理配置在 vite.config.ts 中，所有 /api 开头的请求会被代理到 http://localhost:8000

