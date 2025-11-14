from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Config, User
from schemas import ConfigCreate, ConfigUpdate


def get_config(db: Session, config_id: int):
    """获取单个配置"""
    return db.query(Config).filter(Config.id == config_id).first()


def get_config_by_key(db: Session, config_key: str):
    """根据配置键获取配置"""
    return db.query(Config).filter(Config.config_key == config_key).first()


def get_configs(db: Session, skip: int = 0, limit: int = 100, config_key: str = None, config_value: str = None):
    """分页查询配置列表，支持按配置键和配置值搜索"""
    query = db.query(Config)
    
    if config_key:
        query = query.filter(Config.config_key.like(f"%{config_key}%"))
    
    if config_value:
        query = query.filter(Config.config_value.like(f"%{config_value}%"))
    
    return query.offset(skip).limit(limit).all()


def get_configs_count(db: Session, config_key: str = None, config_value: str = None):
    """获取配置总数"""
    query = db.query(Config)
    
    if config_key:
        query = query.filter(Config.config_key.like(f"%{config_key}%"))
    
    if config_value:
        query = query.filter(Config.config_value.like(f"%{config_value}%"))
    
    return query.count()


def create_config(db: Session, config: ConfigCreate, current_user: User):
    """创建配置"""
    db_config = Config(
        config_key=config.config_key,
        config_value=config.config_value,
        description=config.description or "",
        creator_id=str(current_user.id),
        creator=current_user.username,
        modifier_id=str(current_user.id),
        modifier=current_user.username
    )
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config


def update_config(db: Session, config_id: int, config_update: ConfigUpdate, current_user: User):
    """更新配置"""
    db_config = get_config(db, config_id)
    if db_config:
        if config_update.config_value is not None:
            db_config.config_value = config_update.config_value
        if config_update.description is not None:
            db_config.description = config_update.description
        
        # 更新修改人信息
        db_config.modifier_id = str(current_user.id)
        db_config.modifier = current_user.username
        
        db.commit()
        db.refresh(db_config)
    return db_config


def delete_config(db: Session, config_id: int):
    """删除配置"""
    db_config = get_config(db, config_id)
    if db_config:
        db.delete(db_config)
        db.commit()
        return True
    return False

