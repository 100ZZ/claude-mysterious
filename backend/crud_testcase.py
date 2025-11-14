from sqlalchemy.orm import Session
from models import TestCase, User
from schemas import TestCaseCreate, TestCaseUpdate


def get_testcases(db: Session, skip: int = 0, limit: int = 10, id: int = None, name: str = None, biz: str = None, service: str = None):
    """获取用例列表"""
    query = db.query(TestCase)
    if id:
        query = query.filter(TestCase.id == id)
    if name:
        query = query.filter(TestCase.name.contains(name))
    if biz:
        query = query.filter(TestCase.biz.contains(biz))
    if service:
        query = query.filter(TestCase.service.contains(service))
    return query.offset(skip).limit(limit).all()


def get_testcases_count(db: Session, id: int = None, name: str = None, biz: str = None, service: str = None):
    """获取用例总数"""
    query = db.query(TestCase)
    if id:
        query = query.filter(TestCase.id == id)
    if name:
        query = query.filter(TestCase.name.contains(name))
    if biz:
        query = query.filter(TestCase.biz.contains(biz))
    if service:
        query = query.filter(TestCase.service.contains(service))
    return query.count()


def get_testcase(db: Session, testcase_id: int):
    """根据ID获取用例"""
    return db.query(TestCase).filter(TestCase.id == testcase_id).first()


def create_testcase(db: Session, testcase: TestCaseCreate, current_user: User):
    """创建用例"""
    db_testcase = TestCase(
        name=testcase.name,
        description=testcase.description or "",
        biz=testcase.biz,
        service=testcase.service,
        version=testcase.version,
        status=testcase.status,
        test_case_dir=testcase.test_case_dir or "",
        creator_id=str(current_user.id),
        creator=current_user.username,
        modifier_id=str(current_user.id),
        modifier=current_user.username
    )
    db.add(db_testcase)
    db.commit()
    db.refresh(db_testcase)
    return db_testcase


def update_testcase(db: Session, testcase_id: int, testcase: TestCaseUpdate, current_user: User):
    """更新用例"""
    db_testcase = get_testcase(db, testcase_id)
    if not db_testcase:
        return None
    
    update_data = testcase.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_testcase, field, value)
    
    db_testcase.modifier_id = str(current_user.id)
    db_testcase.modifier = current_user.username
    
    db.commit()
    db.refresh(db_testcase)
    return db_testcase


def delete_testcase(db: Session, testcase_id: int):
    """删除用例"""
    db_testcase = get_testcase(db, testcase_id)
    if not db_testcase:
        return False
    
    db.delete(db_testcase)
    db.commit()
    return True

