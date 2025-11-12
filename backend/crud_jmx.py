from sqlalchemy.orm import Session
from models import Jmx, User
from schemas import JmxCreate, JmxUpdate


def get_jmxs(db: Session, skip: int = 0, limit: int = 10, src_name: str = None, test_case_id: int = None):
    """获取JMX脚本列表"""
    query = db.query(Jmx)
    if src_name:
        query = query.filter(Jmx.src_name.contains(src_name))
    if test_case_id:
        query = query.filter(Jmx.test_case_id == test_case_id)
    return query.offset(skip).limit(limit).all()


def get_jmxs_count(db: Session, src_name: str = None, test_case_id: int = None):
    """获取JMX脚本总数"""
    query = db.query(Jmx)
    if src_name:
        query = query.filter(Jmx.src_name.contains(src_name))
    if test_case_id:
        query = query.filter(Jmx.test_case_id == test_case_id)
    return query.count()


def get_jmx(db: Session, jmx_id: int):
    """根据ID获取JMX脚本"""
    return db.query(Jmx).filter(Jmx.id == jmx_id).first()


def create_jmx(db: Session, jmx: JmxCreate, current_user: User):
    """创建JMX脚本"""
    db_jmx = Jmx(
        src_name=jmx.src_name,
        dst_name=jmx.dst_name or "",
        description=jmx.description or "",
        jmx_dir=jmx.jmx_dir or "",
        test_case_id=jmx.test_case_id,
        jmeter_script_type=jmx.jmeter_script_type,
        jmeter_threads_type=jmx.jmeter_threads_type,
        jmeter_sample_type=jmx.jmeter_sample_type,
        creator_id=str(current_user.id),
        creator=current_user.username,
        modifier_id=str(current_user.id),
        modifier=current_user.username
    )
    db.add(db_jmx)
    db.commit()
    db.refresh(db_jmx)
    return db_jmx


def update_jmx(db: Session, jmx_id: int, jmx: JmxUpdate, current_user: User):
    """更新JMX脚本"""
    db_jmx = get_jmx(db, jmx_id)
    if not db_jmx:
        return None
    
    update_data = jmx.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_jmx, field, value)
    
    db_jmx.modifier_id = str(current_user.id)
    db_jmx.modifier = current_user.username
    
    db.commit()
    db.refresh(db_jmx)
    return db_jmx


def delete_jmx(db: Session, jmx_id: int):
    """删除JMX脚本"""
    db_jmx = get_jmx(db, jmx_id)
    if not db_jmx:
        return False
    
    db.delete(db_jmx)
    db.commit()
    return True

