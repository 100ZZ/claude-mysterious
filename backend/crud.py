from sqlalchemy.orm import Session
from models import User, Config
from schemas import UserCreate, UserUpdate, ConfigCreate, ConfigUpdate
from auth import get_password_hash
from datetime import datetime, timedelta


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100, username: str = None):
    query = db.query(User)
    if username:
        query = query.filter(User.username.like(f"%{username}%"))
    return query.offset(skip).limit(limit).all()


def get_users_count(db: Session, username: str = None):
    query = db.query(User)
    if username:
        query = query.filter(User.username.like(f"%{username}%"))
    return query.count()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    # 设置默认生效时间为当前，失效时间为1年后
    effect_time = datetime.now()
    expire_time = effect_time + timedelta(days=365)
    
    db_user = User(
        username=user.username,
        password=hashed_password,
        real_name=user.real_name or "",
        token="",
        effect_time=effect_time,
        expire_time=expire_time
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data:
            hashed_password = get_password_hash(update_data.pop("password"))
            db_user.password = hashed_password
        
        if "real_name" in update_data:
            db_user.real_name = update_data["real_name"]
        
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

