from sqlalchemy.orm import Session

from model.task import TaskVO


def find_tasks(session: Session, task_group_id: int) -> list[TaskVO]:
    return session.query(TaskVO).filter(TaskVO.task_group_id == task_group_id).all()
