from sqlalchemy.orm import Session
from models import Report, User
from schemas import ReportCreate, ReportUpdate


def get_reports(db: Session, skip: int = 0, limit: int = 10, name: str = None, test_case_id: int = None):
    """获取测试报告列表"""
    query = db.query(Report)
    if name:
        query = query.filter(Report.name.contains(name))
    if test_case_id:
        query = query.filter(Report.test_case_id == test_case_id)
    return query.offset(skip).limit(limit).all()


def get_reports_count(db: Session, name: str = None, test_case_id: int = None):
    """获取测试报告总数"""
    query = db.query(Report)
    if name:
        query = query.filter(Report.name.contains(name))
    if test_case_id:
        query = query.filter(Report.test_case_id == test_case_id)
    return query.count()


def get_report(db: Session, report_id: int):
    """根据ID获取测试报告"""
    return db.query(Report).filter(Report.id == report_id).first()


def create_report(db: Session, report: ReportCreate, current_user: User):
    """创建测试报告"""
    db_report = Report(
        name=report.name,
        description=report.description or "",
        test_case_id=report.test_case_id,
        report_dir=report.report_dir or "",
        exec_type=report.exec_type,
        status=report.status,
        response_data=report.response_data or "",
        jmeter_log_file_path=report.jmeter_log_file_path or "",
        creator_id=str(current_user.id),
        creator=current_user.username,
        modifier_id=str(current_user.id),
        modifier=current_user.username
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def update_report(db: Session, report_id: int, report: ReportUpdate, current_user: User):
    """更新测试报告"""
    db_report = get_report(db, report_id)
    if not db_report:
        return None
    
    update_data = report.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_report, field, value)
    
    db_report.modifier_id = str(current_user.id)
    db_report.modifier = current_user.username
    
    db.commit()
    db.refresh(db_report)
    return db_report


def delete_report(db: Session, report_id: int):
    """删除测试报告"""
    db_report = get_report(db, report_id)
    if not db_report:
        return False
    
    db.delete(db_report)
    db.commit()
    return True

