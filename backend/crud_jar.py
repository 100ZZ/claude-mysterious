from sqlalchemy.orm import Session
from models import Jar, User
from schemas import JarCreate, JarUpdate


def get_jars(db: Session, skip: int = 0, limit: int = 10, src_name: str = None, test_case_id: int = None):
    """获取JAR包列表"""
    query = db.query(Jar)
    if src_name:
        query = query.filter(Jar.src_name.contains(src_name))
    if test_case_id:
        query = query.filter(Jar.test_case_id == test_case_id)
    return query.offset(skip).limit(limit).all()


def get_jars_count(db: Session, src_name: str = None, test_case_id: int = None):
    """获取JAR包总数"""
    query = db.query(Jar)
    if src_name:
        query = query.filter(Jar.src_name.contains(src_name))
    if test_case_id:
        query = query.filter(Jar.test_case_id == test_case_id)
    return query.count()


def get_jar(db: Session, jar_id: int):
    """根据ID获取JAR包"""
    return db.query(Jar).filter(Jar.id == jar_id).first()


def create_jar(db: Session, jar: JarCreate, current_user: User):
    """创建JAR包"""
    db_jar = Jar(
        src_name=jar.src_name,
        dst_name=jar.dst_name or "",
        description=jar.description or "",
        jar_dir=jar.jar_dir or "",
        test_case_id=jar.test_case_id,
        creator_id=str(current_user.id),
        creator=current_user.username,
        modifier_id=str(current_user.id),
        modifier=current_user.username
    )
    db.add(db_jar)
    db.commit()
    db.refresh(db_jar)
    return db_jar


def update_jar(db: Session, jar_id: int, jar: JarUpdate, current_user: User):
    """更新JAR包"""
    db_jar = get_jar(db, jar_id)
    if not db_jar:
        return None
    
    update_data = jar.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_jar, field, value)
    
    db_jar.modifier_id = str(current_user.id)
    db_jar.modifier = current_user.username
    
    db.commit()
    db.refresh(db_jar)
    return db_jar


def delete_jar(db: Session, jar_id: int):
    """删除JAR包"""
    db_jar = get_jar(db, jar_id)
    if not db_jar:
        return False
    
    db.delete(db_jar)
    db.commit()
    return True

