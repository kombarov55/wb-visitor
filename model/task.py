import pydantic
from sqlalchemy import Column, Integer, String, DateTime

from config import database


class TaskVO(database.base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String)
    article = Column(String)
    img = Column(String)
    name = Column(String)
    current_amount = Column(Integer)
    max_amount = Column(Integer)
    interval_in_ms = Column(Integer)
    last_check_date = Column(DateTime, index=True)
    next_check_date = Column(DateTime, index=True)
    status = Column(String, index=True)
    task_group_id = Column(Integer, index=True)


class TaskRs(pydantic.BaseModel):
    id: int
    article: str
    name: str
    img: str
    current_amount: int
    max_amount: int
