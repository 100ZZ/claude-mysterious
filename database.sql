-- Claude Mysterious 数据库初始化脚本
-- 
-- 此脚本用于手动创建数据库和表结构
-- 通常情况下，使用 Python 的 init_db.py 脚本会自动完成初始化
-- 此SQL文件仅作为参考或手动初始化的备选方案

-- 创建数据库
CREATE DATABASE IF NOT EXISTS claude_mysterious 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE claude_mysterious;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    hashed_password VARCHAR(255) NOT NULL COMMENT '加密后的密码',
    email VARCHAR(100) UNIQUE COMMENT '邮箱',
    full_name VARCHAR(100) COMMENT '真实姓名',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    is_admin BOOLEAN DEFAULT FALSE COMMENT '是否管理员',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 注意：密码哈希需要通过应用程序生成
-- 默认管理员账号会在运行 init_db.py 时自动创建
-- 用户名：admin
-- 密码：admin

-- 查看表结构
DESC users;

-- 显示所有表
SHOW TABLES;

