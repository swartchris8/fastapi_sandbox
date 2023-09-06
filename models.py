from enum import Enum
from sqlalchemy import Column, String, Enum as SqlEnum, create_engine

from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "sqlite:///./sql_app.db"
# DATABASE_URL = "postgresql://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class TaskStatusEnum(str, Enum):
    DOES_NOT_EXIST = "does not exist"
    STARTED = "started"
    COMPLETED = "completed"


class TaskStatus(Base):
    __tablename__ = "task_statuses"

    job_id = Column(String, primary_key=True, index=True)
    status = Column(SqlEnum(TaskStatusEnum), index=True)
    result = Column(String)
