from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime

from config import database


class TaskGroupVO(database.base):
    __tablename__ = "task_group"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String)
    target_type = Column(String)
    amount = Column(Integer)
    days = Column(Integer)
    hours = Column(Integer)
    minutes = Column(Integer)
    seconds = Column(Integer)
    interval = Column(Integer)
    status = Column(String)
    end_datetime = Column(DateTime)


class TaskGroupRq(BaseModel):
    task_type: str
    target_type: str
    target_value: str | None = None
    amount: int
    days: int | None = None
    hours: int | None = None
    minutes: int | None = None
    seconds: int | None = None


class TaskGroupRs(TaskGroupRq):
    id: int
    current_amount: int
    status: str
    end_datetime: datetime | None = None
