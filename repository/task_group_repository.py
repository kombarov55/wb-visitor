from sqlalchemy.orm import Session

from model import task_group_status
from model.task_group import TaskGroupRs, TaskGroupVO


def find_task_groups(session: Session, offset: int, limit: int) -> list[TaskGroupRs]:
    xs = session.query(TaskGroupVO).offset(offset).limit(limit).all()
    result = []
    for x in xs:
        rs = TaskGroupRs(
            id=x.id,
            task_type=x.task_type,
            target_type=x.target_type,
            amount=x.amount,
            current_amount=0,
            status=x.status,
            days=x.days,
            hours=x.hours,
            minutes=x.minutes,
            seconds=x.seconds,
            task_status=x.status
        )
        result.append(rs)
    return result
