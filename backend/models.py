from sqlalchemy import Column, BigInteger, String, DateTime, SmallInteger, Text, Boolean
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "mysterious_user"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    username = Column(String(128), nullable=False, default='', unique=True)
    password = Column(String(128), nullable=False, default='')
    real_name = Column(String(128), nullable=False, default='')
    token = Column(String(128), nullable=False, default='')
    effect_time = Column(DateTime, nullable=False, server_default=func.now())
    expire_time = Column(DateTime, nullable=False, server_default=func.now())


class Config(Base):
    __tablename__ = "mysterious_config"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    config_key = Column(String(255), nullable=False, default='', unique=True)
    config_value = Column(String(255), nullable=False, default='')
    description = Column(String(255), nullable=False, default='')
    creator_id = Column(String(32), nullable=False, default='')
    creator = Column(String(32), nullable=False, default='')
    modifier_id = Column(String(32), nullable=False, default='')
    modifier = Column(String(32), nullable=False, default='')
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    modify_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class Node(Base):
    __tablename__ = "mysterious_node"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, default='')
    description = Column(String(255), nullable=False, default='')
    type = Column(SmallInteger, nullable=False, default=0)  # 0-slave，1-master
    host = Column(String(128), nullable=False, default='')
    username = Column(String(128), nullable=False, default='')
    password = Column(String(128), nullable=False, default='')
    port = Column(BigInteger, nullable=False, default=0)
    status = Column(SmallInteger, nullable=False, default=0)  # 0-禁用中，1-启用中
    creator_id = Column(String(32), nullable=False, default='')
    creator = Column(String(32), nullable=False, default='')
    modifier_id = Column(String(32), nullable=False, default='')
    modifier = Column(String(32), nullable=False, default='')
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    modify_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class TestCase(Base):
    __tablename__ = "mysterious_testcase"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, default='')
    description = Column(String(255), nullable=False, default='')
    biz = Column(String(128), nullable=False, default='')
    service = Column(String(128), nullable=False, default='')
    version = Column(String(128), nullable=False, default='')
    status = Column(SmallInteger, nullable=False, default=0)  # 0-未执行，1-执行中, 2-执行成功, 3-执行异常
    test_case_dir = Column(String(255), nullable=False, default='')
    creator_id = Column(String(32), nullable=False, default='')
    creator = Column(String(32), nullable=False, default='')
    modifier_id = Column(String(32), nullable=False, default='')
    modifier = Column(String(32), nullable=False, default='')
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    modify_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class Jmx(Base):
    __tablename__ = "mysterious_jmx"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    src_name = Column(String(255), nullable=False, default='')
    dst_name = Column(String(255), nullable=False, default='')
    description = Column(String(255), nullable=False, default='')
    jmx_dir = Column(String(255), nullable=False, default='')
    test_case_id = Column(BigInteger, nullable=False, default=0)
    jmeter_script_type = Column(SmallInteger, nullable=False, default=0)
    jmeter_threads_type = Column(SmallInteger, nullable=False, default=0)
    jmeter_sample_type = Column(SmallInteger, nullable=False, default=0)
    creator_id = Column(String(32), nullable=False, default='')
    creator = Column(String(32), nullable=False, default='')
    modifier_id = Column(String(32), nullable=False, default='')
    modifier = Column(String(32), nullable=False, default='')
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    modify_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class Jar(Base):
    __tablename__ = "mysterious_jar"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    src_name = Column(String(255), nullable=False, default='')
    dst_name = Column(String(255), nullable=False, default='')
    description = Column(String(255), nullable=False, default='')
    jar_dir = Column(String(255), nullable=False, default='')
    test_case_id = Column(BigInteger, nullable=False, default=0)
    creator_id = Column(String(32), nullable=False, default='')
    creator = Column(String(32), nullable=False, default='')
    modifier_id = Column(String(32), nullable=False, default='')
    modifier = Column(String(32), nullable=False, default='')
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    modify_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class Csv(Base):
    __tablename__ = "mysterious_csv"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    src_name = Column(String(255), nullable=False, default='')
    dst_name = Column(String(255), nullable=False, default='')
    description = Column(String(255), nullable=False, default='')
    csv_dir = Column(String(255), nullable=False, default='')
    test_case_id = Column(BigInteger, nullable=False, default=0)
    creator_id = Column(String(32), nullable=False, default='')
    creator = Column(String(32), nullable=False, default='')
    modifier_id = Column(String(32), nullable=False, default='')
    modifier = Column(String(32), nullable=False, default='')
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    modify_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class Report(Base):
    __tablename__ = "mysterious_report"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, default='')
    description = Column(String(255), nullable=False, default='')
    test_case_id = Column(BigInteger, nullable=False, default=0)
    report_dir = Column(String(255), nullable=False, default='')
    exec_type = Column(SmallInteger, nullable=False, default=1)  # 1-调试, 2-执行
    status = Column(SmallInteger, nullable=False, default=0)  # 0-未执行，1-执行中, 2-执行成功, 3-执行异常
    response_data = Column(String(512), nullable=False, default='')
    jmeter_log_file_path = Column(String(255), nullable=False, default='')
    creator_id = Column(String(32), nullable=False, default='')
    creator = Column(String(32), nullable=False, default='')
    modifier_id = Column(String(32), nullable=False, default='')
    modifier = Column(String(32), nullable=False, default='')
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    modify_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

