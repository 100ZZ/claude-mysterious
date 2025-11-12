from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    real_name: Optional[str] = ""


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    real_name: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    real_name: str
    effect_time: datetime
    expire_time: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# 配置管理相关Schema
class ConfigBase(BaseModel):
    config_key: str
    config_value: str
    description: Optional[str] = ""


class ConfigCreate(ConfigBase):
    pass


class ConfigUpdate(BaseModel):
    config_value: Optional[str] = None
    description: Optional[str] = None


class ConfigResponse(ConfigBase):
    id: int
    creator_id: str
    creator: str
    modifier_id: str
    modifier: str
    create_time: datetime
    modify_time: datetime

    class Config:
        from_attributes = True


# 节点管理相关Schema
class NodeBase(BaseModel):
    name: str
    description: Optional[str] = ""
    type: int = 0  # 0-slave，1-master
    host: str
    username: str
    password: str
    port: int
    status: int = 0  # 0-禁用中，1-启用中


class NodeCreate(NodeBase):
    pass


class NodeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[int] = None
    host: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    port: Optional[int] = None
    status: Optional[int] = None


class NodeResponse(NodeBase):
    id: int
    creator_id: str
    creator: str
    modifier_id: str
    modifier: str
    create_time: datetime
    modify_time: datetime

    class Config:
        from_attributes = True


# 用例管理相关Schema
class TestCaseBase(BaseModel):
    name: str
    description: Optional[str] = ""
    biz: str
    service: str
    version: str
    status: int = 0  # 0-未执行，1-执行中, 2-执行成功, 3-执行异常
    test_case_dir: Optional[str] = ""


class TestCaseCreate(TestCaseBase):
    pass


class TestCaseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    biz: Optional[str] = None
    service: Optional[str] = None
    version: Optional[str] = None
    status: Optional[int] = None
    test_case_dir: Optional[str] = None


class TestCaseResponse(TestCaseBase):
    id: int
    creator_id: str
    creator: str
    modifier_id: str
    modifier: str
    create_time: datetime
    modify_time: datetime

    class Config:
        from_attributes = True


# JMX脚本管理相关Schema
class JmxBase(BaseModel):
    src_name: str
    dst_name: Optional[str] = ""
    description: Optional[str] = ""
    jmx_dir: Optional[str] = ""
    test_case_id: int
    jmeter_script_type: int = 0
    jmeter_threads_type: int = 0
    jmeter_sample_type: int = 0


class JmxCreate(JmxBase):
    pass


class JmxUpdate(BaseModel):
    src_name: Optional[str] = None
    dst_name: Optional[str] = None
    description: Optional[str] = None
    jmx_dir: Optional[str] = None
    test_case_id: Optional[int] = None
    jmeter_script_type: Optional[int] = None
    jmeter_threads_type: Optional[int] = None
    jmeter_sample_type: Optional[int] = None


class JmxResponse(JmxBase):
    id: int
    creator_id: str
    creator: str
    modifier_id: str
    modifier: str
    create_time: datetime
    modify_time: datetime

    class Config:
        from_attributes = True


# JAR包管理相关Schema
class JarBase(BaseModel):
    src_name: str
    dst_name: Optional[str] = ""
    description: Optional[str] = ""
    jar_dir: Optional[str] = ""
    test_case_id: int


class JarCreate(JarBase):
    pass


class JarUpdate(BaseModel):
    src_name: Optional[str] = None
    dst_name: Optional[str] = None
    description: Optional[str] = None
    jar_dir: Optional[str] = None
    test_case_id: Optional[int] = None


class JarResponse(JarBase):
    id: int
    creator_id: str
    creator: str
    modifier_id: str
    modifier: str
    create_time: datetime
    modify_time: datetime

    class Config:
        from_attributes = True


# CSV文件管理相关Schema
class CsvBase(BaseModel):
    src_name: str
    dst_name: Optional[str] = ""
    description: Optional[str] = ""
    csv_dir: Optional[str] = ""
    test_case_id: int


class CsvCreate(CsvBase):
    pass


class CsvUpdate(BaseModel):
    src_name: Optional[str] = None
    dst_name: Optional[str] = None
    description: Optional[str] = None
    csv_dir: Optional[str] = None
    test_case_id: Optional[int] = None


class CsvResponse(CsvBase):
    id: int
    creator_id: str
    creator: str
    modifier_id: str
    modifier: str
    create_time: datetime
    modify_time: datetime

    class Config:
        from_attributes = True


# 测试报告管理相关Schema
class ReportBase(BaseModel):
    name: str
    description: Optional[str] = ""
    test_case_id: int
    report_dir: Optional[str] = ""
    exec_type: int = 1  # 1-调试, 2-执行
    status: int = 0  # 0-未执行，1-执行中, 2-执行成功, 3-执行异常
    response_data: Optional[str] = ""
    jmeter_log_file_path: Optional[str] = ""


class ReportCreate(ReportBase):
    pass


class ReportUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    test_case_id: Optional[int] = None
    report_dir: Optional[str] = None
    exec_type: Optional[int] = None
    status: Optional[int] = None
    response_data: Optional[str] = None
    jmeter_log_file_path: Optional[str] = None


class ReportResponse(ReportBase):
    id: int
    creator_id: str
    creator: str
    modifier_id: str
    modifier: str
    create_time: datetime
    modify_time: datetime

    class Config:
        from_attributes = True

