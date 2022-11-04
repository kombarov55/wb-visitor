from sqlalchemy.orm import Session
from sqlalchemy import func

from model import task_group_status
from model.task import TaskVO, TaskRs
from model.task_group import TaskGroupRs, TaskGroupVO, TaskGroupShortRs
from repository import task_repository


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


def find_task_groups_short(session: Session, offset: int, limit: int) -> list[TaskGroupShortRs]:
    xs = session.query(TaskGroupVO).offset(offset).limit(limit).all()
    result = []
    for x in xs:
        max_amount = None
        current_amount = 0
        if x.status != task_group_status.preparing:
            max_amount = count_max_amount(session, x.id, x.amount)
            current_amount = count_current_amount(session, x.id)
        rs = TaskGroupShortRs(
            id=x.id,
            task_type=x.task_type,
            current_amount=current_amount,
            max_amount=max_amount,
            status=x.status
        )
        result.append(rs)
    return result


def find_task_group_by_id(session: Session, task_group_id: int) -> TaskGroupRs:
    vo = session.query(TaskGroupVO).filter(TaskGroupVO.id == task_group_id).first()
    tasks = task_repository.find_tasks(session, task_group_id)

    return TaskGroupRs(
        id=vo.id,
        task_type=vo.task_type,
        target_type=vo.target_type,
        target_value=vo.target_value,
        amount=vo.amount,
        current_amount=0,
        max_amount=vo.max_amount,
        status=vo.status,
        days=vo.days,
        hours=vo.hours,
        minutes=vo.minutes,
        seconds=vo.seconds,
        task_status=vo.status,
        start_datetime=vo.start_datetime,
        end_datetime=vo.end_datetime,
        task_count=vo.task_count,
        tasks=list(map(lambda v: TaskRs(
            id=v.id,
            article=v.article,
            name=v.name,
            img=v.img,
            current_amount=v.current_amount,
            max_amount=v.max_amount
        ), tasks))
    )


def count_current_amount(session: Session, task_group_id: int) -> int:
    return session.query(func.sum(TaskVO.current_amount)).filter(TaskVO.task_group_id == task_group_id).scalar()


def count_max_amount(session: Session, task_group_id: int, amount: int) -> int:
    return session.query(TaskVO).filter(TaskVO.task_group_id == task_group_id).count() * amount
