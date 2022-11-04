from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime

from config import database
from model.task import TaskRs


class TaskGroupVO(database.base):
    __tablename__ = "task_group"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String)
    target_type = Column(String)
    target_value = Column(String)
    amount = Column(Integer)
    max_amount = Column(Integer)
    task_count = Column(Integer)
    days = Column(Integer)
    hours = Column(Integer)
    minutes = Column(Integer)
    seconds = Column(Integer)
    interval = Column(Integer)
    status = Column(String)
    start_datetime = Column(DateTime)
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
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
    max_amount: int | None = None
    tasks: list[TaskRs] | None = None
    task_count: int | None = None


class TaskGroupShortRs(BaseModel):
    id: int
    task_type: str
    current_amount: int
    max_amount: int | None = None
    status: str
