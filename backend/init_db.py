#!/usr/bin/env python3
"""
数据库初始化脚本
创建数据库表并添加默认的admin用户
"""
from database import engine, SessionLocal, Base
from models import User
from auth import get_password_hash
from datetime import datetime, timedelta


def init_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    print("Creating default admin user...")
    db = SessionLocal()
    try:
        # 检查admin用户是否已存在
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            effect_time = datetime.now()
            expire_time = effect_time + timedelta(days=36500)  # 100年有效期
            
            admin = User(
                username="admin",
                password=get_password_hash("admin"),
                real_name="系统管理员",
                token="",
                effect_time=effect_time,
                expire_time=expire_time
            )
            db.add(admin)
            db.commit()
            print("Default admin user created successfully!")
            print("Username: admin")
            print("Password: admin")
            print("Real Name: 系统管理员")
        else:
            print("Admin user already exists!")
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()

