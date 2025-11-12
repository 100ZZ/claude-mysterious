from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List, Optional

from database import get_db
from models import User, Config, Node, TestCase, Jmx, Jar, Csv, Report
from schemas import (
    UserCreate, UserUpdate, UserResponse, Token, LoginRequest,
    ConfigCreate, ConfigUpdate, ConfigResponse,
    NodeCreate, NodeUpdate, NodeResponse,
    TestCaseCreate, TestCaseUpdate, TestCaseResponse,
    JmxCreate, JmxUpdate, JmxResponse,
    JarCreate, JarUpdate, JarResponse,
    CsvCreate, CsvUpdate, CsvResponse,
    ReportCreate, ReportUpdate, ReportResponse
)
from auth import (
    verify_password,
    create_access_token,
    get_current_active_user,
    get_admin_user
)
from config import get_settings
import crud
import crud_config
import crud_node
import crud_testcase
import crud_jmx
import crud_jar
import crud_csv
import crud_report

settings = get_settings()

app = FastAPI(title="Claude Mysterious API", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:1212", "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Claude Mysterious API"}


@app.post("/api/auth/login", response_model=Token)
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=login_request.username)
    if not user or not verify_password(login_request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查账号是否过期
    from datetime import datetime
    if user.expire_time < datetime.now():
        raise HTTPException(status_code=400, detail="User account expired")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # 更新用户token
    user.token = access_token
    db.commit()
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/auth/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/api/users", response_model=dict)
def read_users(
    page: int = 1,
    size: int = 10,
    username: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """分页查询用户列表"""
    skip = (page - 1) * size
    users = crud.get_users(db, skip=skip, limit=size, username=username)
    total = crud.get_users_count(db, username=username)
    
    # 将ORM对象转换为Pydantic schema对象
    users_list = [UserResponse.model_validate(user) for user in users]
    
    return {
        "list": users_list,
        "page": page,
        "size": size,
        "total": total
    }


@app.get("/api/users/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    return crud.create_user(db=db, user=user)


@app.put("/api/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.update_user(db=db, user_id=user_id, user_update=user)


@app.delete("/api/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    if not crud.delete_user(db, user_id=user_id):
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}


# ==================== 配置管理接口 ====================

@app.get("/api/configs", response_model=dict)
def read_configs(
    page: int = 1,
    size: int = 10,
    config_key: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """分页查询配置列表"""
    skip = (page - 1) * size
    configs = crud_config.get_configs(db, skip=skip, limit=size, config_key=config_key)
    total = crud_config.get_configs_count(db, config_key=config_key)
    
    # 将ORM对象转换为Pydantic schema对象
    configs_list = [ConfigResponse.model_validate(config) for config in configs]
    
    return {
        "list": configs_list,
        "page": page,
        "size": size,
        "total": total
    }


@app.get("/api/configs/{config_id}", response_model=ConfigResponse)
def read_config(
    config_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取配置详情"""
    db_config = crud_config.get_config(db, config_id=config_id)
    if db_config is None:
        raise HTTPException(status_code=404, detail="Config not found")
    return db_config


@app.post("/api/configs", response_model=ConfigResponse, status_code=status.HTTP_201_CREATED)
def create_config(
    config: ConfigCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """新增配置（需要管理员权限）"""
    # 检查配置键是否已存在
    db_config = crud_config.get_config_by_key(db, config_key=config.config_key)
    if db_config:
        raise HTTPException(status_code=400, detail="Config key already exists")
    
    return crud_config.create_config(db=db, config=config, current_user=current_user)


@app.put("/api/configs/{config_id}", response_model=ConfigResponse)
def update_config(
    config_id: int,
    config: ConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """修改配置（需要管理员权限）"""
    db_config = crud_config.get_config(db, config_id=config_id)
    if db_config is None:
        raise HTTPException(status_code=404, detail="Config not found")
    
    return crud_config.update_config(db=db, config_id=config_id, config_update=config, current_user=current_user)


@app.delete("/api/configs/{config_id}")
def delete_config(
    config_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """删除配置（需要管理员权限）"""
    if not crud_config.delete_config(db, config_id=config_id):
        raise HTTPException(status_code=404, detail="Config not found")
    
    return {"message": "Config deleted successfully"}


# ==================== 节点管理接口 ====================

@app.get("/api/nodes", response_model=dict)
def read_nodes(
    page: int = 1,
    size: int = 10,
    name: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """分页查询节点列表"""
    skip = (page - 1) * size
    nodes = crud_node.get_nodes(db, skip=skip, limit=size, name=name)
    total = crud_node.get_nodes_count(db, name=name)
    
    nodes_list = [NodeResponse.model_validate(node) for node in nodes]
    
    return {
        "list": nodes_list,
        "page": page,
        "size": size,
        "total": total
    }


@app.get("/api/nodes/{node_id}", response_model=NodeResponse)
def read_node(
    node_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """根据ID查询节点"""
    db_node = crud_node.get_node(db, node_id=node_id)
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    
    return db_node


@app.post("/api/nodes", response_model=NodeResponse, status_code=status.HTTP_201_CREATED)
def create_node(
    node: NodeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """新增节点"""
    return crud_node.create_node(db=db, node=node, current_user=current_user)


@app.put("/api/nodes/{node_id}", response_model=NodeResponse)
def update_node(
    node_id: int,
    node: NodeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """修改节点"""
    db_node = crud_node.get_node(db, node_id=node_id)
    if db_node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    
    return crud_node.update_node(db=db, node_id=node_id, node=node, current_user=current_user)


@app.delete("/api/nodes/{node_id}")
def delete_node(
    node_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除节点"""
    if not crud_node.delete_node(db, node_id=node_id):
        raise HTTPException(status_code=404, detail="Node not found")
    
    return {"message": "Node deleted successfully"}


# ==================== 用例管理接口 ====================

@app.get("/api/testcases", response_model=dict)
def read_testcases(
    page: int = 1,
    size: int = 10,
    name: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """分页查询用例列表"""
    skip = (page - 1) * size
    testcases = crud_testcase.get_testcases(db, skip=skip, limit=size, name=name)
    total = crud_testcase.get_testcases_count(db, name=name)
    
    testcases_list = [TestCaseResponse.model_validate(testcase) for testcase in testcases]
    
    return {
        "list": testcases_list,
        "page": page,
        "size": size,
        "total": total
    }


@app.get("/api/testcases/{testcase_id}", response_model=TestCaseResponse)
def read_testcase(
    testcase_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """根据ID查询用例"""
    db_testcase = crud_testcase.get_testcase(db, testcase_id=testcase_id)
    if db_testcase is None:
        raise HTTPException(status_code=404, detail="TestCase not found")
    
    return db_testcase


@app.post("/api/testcases", response_model=TestCaseResponse, status_code=status.HTTP_201_CREATED)
def create_testcase(
    testcase: TestCaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """新增用例"""
    return crud_testcase.create_testcase(db=db, testcase=testcase, current_user=current_user)


@app.put("/api/testcases/{testcase_id}", response_model=TestCaseResponse)
def update_testcase(
    testcase_id: int,
    testcase: TestCaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """修改用例"""
    db_testcase = crud_testcase.get_testcase(db, testcase_id=testcase_id)
    if db_testcase is None:
        raise HTTPException(status_code=404, detail="TestCase not found")
    
    return crud_testcase.update_testcase(db=db, testcase_id=testcase_id, testcase=testcase, current_user=current_user)


@app.delete("/api/testcases/{testcase_id}")
def delete_testcase(
    testcase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除用例"""
    if not crud_testcase.delete_testcase(db, testcase_id=testcase_id):
        raise HTTPException(status_code=404, detail="TestCase not found")
    
    return {"message": "TestCase deleted successfully"}


# ==================== JMX脚本管理接口 ====================

@app.get("/api/jmxs", response_model=dict)
def read_jmxs(
    page: int = 1,
    size: int = 10,
    src_name: Optional[str] = None,
    test_case_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """分页查询JMX脚本列表"""
    skip = (page - 1) * size
    jmxs = crud_jmx.get_jmxs(db, skip=skip, limit=size, src_name=src_name, test_case_id=test_case_id)
    total = crud_jmx.get_jmxs_count(db, src_name=src_name, test_case_id=test_case_id)
    
    jmxs_list = [JmxResponse.model_validate(jmx) for jmx in jmxs]
    
    return {
        "list": jmxs_list,
        "page": page,
        "size": size,
        "total": total
    }


@app.get("/api/jmxs/{jmx_id}", response_model=JmxResponse)
def read_jmx(
    jmx_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """根据ID查询JMX脚本"""
    db_jmx = crud_jmx.get_jmx(db, jmx_id=jmx_id)
    if db_jmx is None:
        raise HTTPException(status_code=404, detail="Jmx not found")
    
    return db_jmx


@app.post("/api/jmxs", response_model=JmxResponse, status_code=status.HTTP_201_CREATED)
def create_jmx(
    jmx: JmxCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """新增JMX脚本"""
    return crud_jmx.create_jmx(db=db, jmx=jmx, current_user=current_user)


@app.put("/api/jmxs/{jmx_id}", response_model=JmxResponse)
def update_jmx(
    jmx_id: int,
    jmx: JmxUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """修改JMX脚本"""
    db_jmx = crud_jmx.get_jmx(db, jmx_id=jmx_id)
    if db_jmx is None:
        raise HTTPException(status_code=404, detail="Jmx not found")
    
    return crud_jmx.update_jmx(db=db, jmx_id=jmx_id, jmx=jmx, current_user=current_user)


@app.delete("/api/jmxs/{jmx_id}")
def delete_jmx(
    jmx_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除JMX脚本"""
    if not crud_jmx.delete_jmx(db, jmx_id=jmx_id):
        raise HTTPException(status_code=404, detail="Jmx not found")
    
    return {"message": "Jmx deleted successfully"}


# ==================== JAR包管理接口 ====================

@app.get("/api/jars", response_model=dict)
def read_jars(
    page: int = 1,
    size: int = 10,
    src_name: Optional[str] = None,
    test_case_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """分页查询JAR包列表"""
    skip = (page - 1) * size
    jars = crud_jar.get_jars(db, skip=skip, limit=size, src_name=src_name, test_case_id=test_case_id)
    total = crud_jar.get_jars_count(db, src_name=src_name, test_case_id=test_case_id)
    
    jars_list = [JarResponse.model_validate(jar) for jar in jars]
    
    return {
        "list": jars_list,
        "page": page,
        "size": size,
        "total": total
    }


@app.get("/api/jars/{jar_id}", response_model=JarResponse)
def read_jar(
    jar_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """根据ID查询JAR包"""
    db_jar = crud_jar.get_jar(db, jar_id=jar_id)
    if db_jar is None:
        raise HTTPException(status_code=404, detail="Jar not found")
    
    return db_jar


@app.post("/api/jars", response_model=JarResponse, status_code=status.HTTP_201_CREATED)
def create_jar(
    jar: JarCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """新增JAR包"""
    return crud_jar.create_jar(db=db, jar=jar, current_user=current_user)


@app.put("/api/jars/{jar_id}", response_model=JarResponse)
def update_jar(
    jar_id: int,
    jar: JarUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """修改JAR包"""
    db_jar = crud_jar.get_jar(db, jar_id=jar_id)
    if db_jar is None:
        raise HTTPException(status_code=404, detail="Jar not found")
    
    return crud_jar.update_jar(db=db, jar_id=jar_id, jar=jar, current_user=current_user)


@app.delete("/api/jars/{jar_id}")
def delete_jar(
    jar_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除JAR包"""
    if not crud_jar.delete_jar(db, jar_id=jar_id):
        raise HTTPException(status_code=404, detail="Jar not found")
    
    return {"message": "Jar deleted successfully"}


# ==================== CSV文件管理接口 ====================

@app.get("/api/csvs", response_model=dict)
def read_csvs(
    page: int = 1,
    size: int = 10,
    src_name: Optional[str] = None,
    test_case_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """分页查询CSV文件列表"""
    skip = (page - 1) * size
    csvs = crud_csv.get_csvs(db, skip=skip, limit=size, src_name=src_name, test_case_id=test_case_id)
    total = crud_csv.get_csvs_count(db, src_name=src_name, test_case_id=test_case_id)
    
    csvs_list = [CsvResponse.model_validate(csv) for csv in csvs]
    
    return {
        "list": csvs_list,
        "page": page,
        "size": size,
        "total": total
    }


@app.get("/api/csvs/{csv_id}", response_model=CsvResponse)
def read_csv(
    csv_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """根据ID查询CSV文件"""
    db_csv = crud_csv.get_csv(db, csv_id=csv_id)
    if db_csv is None:
        raise HTTPException(status_code=404, detail="Csv not found")
    
    return db_csv


@app.post("/api/csvs", response_model=CsvResponse, status_code=status.HTTP_201_CREATED)
def create_csv(
    csv: CsvCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """新增CSV文件"""
    return crud_csv.create_csv(db=db, csv=csv, current_user=current_user)


@app.put("/api/csvs/{csv_id}", response_model=CsvResponse)
def update_csv(
    csv_id: int,
    csv: CsvUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """修改CSV文件"""
    db_csv = crud_csv.get_csv(db, csv_id=csv_id)
    if db_csv is None:
        raise HTTPException(status_code=404, detail="Csv not found")
    
    return crud_csv.update_csv(db=db, csv_id=csv_id, csv=csv, current_user=current_user)


@app.delete("/api/csvs/{csv_id}")
def delete_csv(
    csv_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除CSV文件"""
    if not crud_csv.delete_csv(db, csv_id=csv_id):
        raise HTTPException(status_code=404, detail="Csv not found")
    
    return {"message": "Csv deleted successfully"}


# ==================== 测试报告管理接口 ====================

@app.get("/api/reports", response_model=dict)
def read_reports(
    page: int = 1,
    size: int = 10,
    name: Optional[str] = None,
    test_case_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """分页查询测试报告列表"""
    skip = (page - 1) * size
    reports = crud_report.get_reports(db, skip=skip, limit=size, name=name, test_case_id=test_case_id)
    total = crud_report.get_reports_count(db, name=name, test_case_id=test_case_id)
    
    reports_list = [ReportResponse.model_validate(report) for report in reports]
    
    return {
        "list": reports_list,
        "page": page,
        "size": size,
        "total": total
    }


@app.get("/api/reports/{report_id}", response_model=ReportResponse)
def read_report(
    report_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """根据ID查询测试报告"""
    db_report = crud_report.get_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return db_report


@app.post("/api/reports", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(
    report: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """新增测试报告"""
    return crud_report.create_report(db=db, report=report, current_user=current_user)


@app.put("/api/reports/{report_id}", response_model=ReportResponse)
def update_report(
    report_id: int,
    report: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """修改测试报告"""
    db_report = crud_report.get_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return crud_report.update_report(db=db, report_id=report_id, report=report, current_user=current_user)


@app.delete("/api/reports/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除测试报告"""
    if not crud_report.delete_report(db, report_id=report_id):
        raise HTTPException(status_code=404, detail="Report not found")
    
    return {"message": "Report deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=2121)

