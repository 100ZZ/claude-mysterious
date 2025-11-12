from sqlalchemy.orm import Session
from models import Csv, User
from schemas import CsvCreate, CsvUpdate


def get_csvs(db: Session, skip: int = 0, limit: int = 10, src_name: str = None, test_case_id: int = None):
    """获取CSV文件列表"""
    query = db.query(Csv)
    if src_name:
        query = query.filter(Csv.src_name.contains(src_name))
    if test_case_id:
        query = query.filter(Csv.test_case_id == test_case_id)
    return query.offset(skip).limit(limit).all()


def get_csvs_count(db: Session, src_name: str = None, test_case_id: int = None):
    """获取CSV文件总数"""
    query = db.query(Csv)
    if src_name:
        query = query.filter(Csv.src_name.contains(src_name))
    if test_case_id:
        query = query.filter(Csv.test_case_id == test_case_id)
    return query.count()


def get_csv(db: Session, csv_id: int):
    """根据ID获取CSV文件"""
    return db.query(Csv).filter(Csv.id == csv_id).first()


def create_csv(db: Session, csv: CsvCreate, current_user: User):
    """创建CSV文件"""
    db_csv = Csv(
        src_name=csv.src_name,
        dst_name=csv.dst_name or "",
        description=csv.description or "",
        csv_dir=csv.csv_dir or "",
        test_case_id=csv.test_case_id,
        creator_id=str(current_user.id),
        creator=current_user.username,
        modifier_id=str(current_user.id),
        modifier=current_user.username
    )
    db.add(db_csv)
    db.commit()
    db.refresh(db_csv)
    return db_csv


def update_csv(db: Session, csv_id: int, csv: CsvUpdate, current_user: User):
    """更新CSV文件"""
    db_csv = get_csv(db, csv_id)
    if not db_csv:
        return None
    
    update_data = csv.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_csv, field, value)
    
    db_csv.modifier_id = str(current_user.id)
    db_csv.modifier = current_user.username
    
    db.commit()
    db.refresh(db_csv)
    return db_csv


def delete_csv(db: Session, csv_id: int):
    """删除CSV文件"""
    db_csv = get_csv(db, csv_id)
    if not db_csv:
        return False
    
    db.delete(db_csv)
    db.commit()
    return True

