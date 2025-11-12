# 部署指南 🚀

本指南帮助你将 Claude Mysterious 系统部署到生产环境。

## 📋 部署准备

### 服务器要求

**最低配置**：
- CPU: 2核
- 内存: 4GB
- 硬盘: 20GB
- 操作系统: Ubuntu 20.04+ / CentOS 7+ / macOS

**推荐配置**：
- CPU: 4核+
- 内存: 8GB+
- 硬盘: 50GB+
- SSD存储

### 软件要求

- Python 3.8+
- Node.js 16+
- MySQL 8.0
- Nginx
- Supervisor (进程管理) 或 systemd

---

## 🌐 方式一：传统部署

### 1. 服务器准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y  # Ubuntu/Debian
# 或
sudo yum update -y  # CentOS

# 安装必要软件
sudo apt install -y python3 python3-pip python3-venv nodejs npm nginx supervisor mysql-server
```

### 2. 数据库设置

```bash
# 登录MySQL
sudo mysql -u root -p

# 创建数据库
CREATE DATABASE claude_mysterious CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建专用数据库用户（生产环境）
CREATE USER 'claudeuser'@'localhost' IDENTIFIED BY 'your_strong_password_here';
GRANT ALL PRIVILEGES ON claude_mysterious.* TO 'claudeuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. 部署后端

```bash
# 创建部署目录
sudo mkdir -p /var/www/claude-mysterious
cd /var/www/claude-mysterious

# 上传代码（使用git或scp）
git clone <your-repo-url> .
# 或
scp -r ./backend user@server:/var/www/claude-mysterious/

# 后端设置
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 配置环境变量
cat > .env << EOF
DATABASE_URL=mysql+pymysql://claudeuser:your_strong_password_here@localhost:3306/claude_mysterious
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF

# 初始化数据库
python init_db.py

# 测试运行
python main.py
# 按Ctrl+C停止
```

### 4. 配置 Supervisor（后端进程管理）

```bash
# 创建supervisor配置
sudo nano /etc/supervisor/conf.d/claude-backend.conf
```

**配置内容**：
```ini
[program:claude-backend]
directory=/var/www/claude-mysterious/backend
command=/var/www/claude-mysterious/backend/venv/bin/python main.py
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/claude-backend.err.log
stdout_logfile=/var/log/claude-backend.out.log
environment=PATH="/var/www/claude-mysterious/backend/venv/bin"
```

```bash
# 重载supervisor配置
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start claude-backend

# 查看状态
sudo supervisorctl status claude-backend
```

### 5. 部署前端

```bash
cd /var/www/claude-mysterious/frontend

# 安装依赖
npm install

# 构建生产版本
npm run build

# 此时会生成 dist 目录
```

### 6. 配置 Nginx

```bash
# 创建Nginx配置
sudo nano /etc/nginx/sites-available/claude-mysterious
```

**配置内容**：
```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名或IP

    # 前端
    location / {
        root /var/www/claude-mysterious/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API文档
    location /docs {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }

    # 日志
    access_log /var/log/nginx/claude-mysterious.access.log;
    error_log /var/log/nginx/claude-mysterious.error.log;
}
```

```bash
# 启用站点
sudo ln -s /etc/nginx/sites-available/claude-mysterious /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重载Nginx
sudo systemctl reload nginx
```

### 7. 配置 SSL（推荐）

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d your-domain.com

# 证书会自动续期
sudo certbot renew --dry-run
```

---

## 🐳 方式二：Docker部署（推荐）

### 1. 创建 Dockerfile（后端）

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
```

### 2. 创建 Dockerfile（前端）

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 3. 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: Test@123456
      MYSQL_DATABASE: claude_mysterious
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"
    networks:
      - claude-network

  backend:
    build: ./backend
    environment:
      DATABASE_URL: mysql+pymysql://root:Test@123456@mysql:3306/claude_mysterious
      SECRET_KEY: your-secret-key-change-this
      ALGORITHM: HS256
      ACCESS_TOKEN_EXPIRE_MINUTES: 30
    ports:
      - "8000:8000"
    depends_on:
      - mysql
    networks:
      - claude-network

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - claude-network

volumes:
  mysql_data:

networks:
  claude-network:
    driver: bridge
```

### 4. 启动服务

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 停止并删除数据
docker-compose down -v
```

---

## ☁️ 方式三：云服务部署

### AWS 部署

1. **EC2**: 使用传统部署方式
2. **RDS**: MySQL数据库
3. **S3**: 静态文件存储
4. **CloudFront**: CDN加速
5. **Route53**: 域名管理

### 阿里云部署

1. **ECS**: 云服务器
2. **RDS**: 云数据库
3. **OSS**: 对象存储
4. **CDN**: 内容分发

### 腾讯云部署

1. **CVM**: 云服务器
2. **TencentDB**: 云数据库
3. **COS**: 对象存储
4. **CDN**: 内容分发

---

## 🔒 生产环境安全建议

### 1. 环境变量

```bash
# 生成强密钥
SECRET_KEY=$(openssl rand -hex 32)

# 使用环境变量而非硬编码
export DATABASE_URL="..."
export SECRET_KEY="..."
```

### 2. 数据库安全

- 使用强密码
- 限制远程访问
- 定期备份
- 启用慢查询日志

```bash
# 数据库备份脚本
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u root -p claude_mysterious > backup_$DATE.sql
```

### 3. 防火墙配置

```bash
# 使用ufw
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# 禁止MySQL远程访问
sudo ufw deny 3306/tcp
```

### 4. 应用安全

- 修改默认管理员密码
- 启用HTTPS
- 配置CORS白名单
- 添加API限流
- 启用日志记录
- 定期更新依赖

### 5. 监控和日志

```bash
# 查看后端日志
sudo tail -f /var/log/claude-backend.out.log

# 查看Nginx日志
sudo tail -f /var/log/nginx/claude-mysterious.access.log

# 查看系统资源
htop
```

---

## 📊 性能优化

### 后端优化

1. **使用Gunicorn**（生产环境）

```bash
# 安装gunicorn
pip install gunicorn

# 运行（4个worker进程）
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

2. **数据库连接池**
已在SQLAlchemy中配置

3. **启用缓存**
考虑使用Redis缓存频繁查询的数据

### 前端优化

1. **代码分割**
Vite自动处理

2. **CDN加速**
将静态资源部署到CDN

3. **Gzip压缩**
Nginx配置：

```nginx
gzip on;
gzip_vary on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
```

---

## 🔄 持续部署

### GitHub Actions 示例

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /var/www/claude-mysterious
            git pull
            cd backend
            source venv/bin/activate
            pip install -r requirements.txt
            sudo supervisorctl restart claude-backend
            cd ../frontend
            npm install
            npm run build
            sudo systemctl reload nginx
```

---

## ✅ 部署检查清单

### 部署前

- [ ] 代码已测试
- [ ] 数据库已备份
- [ ] 环境变量已配置
- [ ] SSL证书已准备
- [ ] 域名已解析

### 部署后

- [ ] 应用可以访问
- [ ] API正常工作
- [ ] 数据库连接正常
- [ ] 日志正常输出
- [ ] SSL证书有效
- [ ] 修改默认密码
- [ ] 配置备份计划
- [ ] 设置监控告警

---

## 📞 故障排查

### 后端无法启动

```bash
# 查看日志
sudo supervisorctl tail -f claude-backend stderr

# 检查进程
ps aux | grep python

# 检查端口
netstat -tlnp | grep 8000
```

### 前端无法访问

```bash
# 检查Nginx状态
sudo systemctl status nginx

# 查看错误日志
sudo tail -f /var/log/nginx/error.log

# 检查文件权限
ls -la /var/www/claude-mysterious/frontend/dist
```

### 数据库连接失败

```bash
# 检查MySQL状态
sudo systemctl status mysql

# 测试连接
mysql -h localhost -u claudeuser -p claude_mysterious
```

---

## 📚 相关文档

- [README.md](./README.md) - 项目总览
- [INSTALL.md](./INSTALL.md) - 本地安装
- [API_EXAMPLES.md](./API_EXAMPLES.md) - API使用

---

**祝部署顺利！** 🎉

