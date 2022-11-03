from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from model import task_target, task_status, task_group_status
from model.task import TaskVO
from model.task_group import TaskGroupRq, TaskGroupVO, TaskGroupRs
from service import wb_service


def add_task_group(rq: TaskGroupRq, session: Session, background_tasks: BackgroundTasks) -> TaskGroupRs:
    interval_in_ms = calculate_interval(rq.days, rq.hours, rq.minutes, rq.seconds)

    task_group_vo = TaskGroupVO(
        task_type=rq.task_type,
        target_type=rq.target_type,
        amount=rq.amount,
        interval=interval_in_ms,
        days=rq.days,
        hours=rq.hours,
        minutes=rq.minutes,
        seconds=rq.seconds,
        status=task_group_status.preparing
    )

    session.add(task_group_vo)
    session.commit()
    session.refresh(task_group_vo)

    background_tasks.add_task(add_tasks, rq, task_group_id=task_group_vo.id, session=session)

    return TaskGroupRs(
        id=task_group_vo.id,
        task_type=rq.task_type,
        target_type=rq.target_type,
        amount=rq.amount,
        current_amount=0,
        status=task_group_status.preparing,
        days=rq.days,
        hours=rq.hours,
        minutes=rq.minutes,
        seconds=rq.seconds,
        task_status=task_group_vo.status
    )


def add_tasks(rq: TaskGroupRq, task_group_id: int, session: Session):
    interval_in_ms = calculate_interval(rq.days, rq.hours, rq.minutes, rq.seconds)
    xs = get_articles(rq.target_type, rq.target_value)

    for x in xs:
        article, name, src = x
        task_vo = TaskVO(
            task_type=rq.task_type,
            article=article,
            name=name,
            img=src,
            current_amount=0,
            target_amount=rq.amount,
            interval_in_ms=interval_in_ms,
            next_check_date=calculate_next_check_date(interval_in_ms),
            status=task_status.scheduled,
            task_group_id=task_group_id
        )
        session.add(task_vo)
    task_group_vo = session.query(TaskGroupVO).filter(TaskGroupVO.id == task_group_id).first()
    task_group_vo.status = task_group_status.running
    task_group_vo.end_datetime = calculate_endtime(interval_in_ms, len(xs))
    session.commit()


def calculate_next_check_date(interval_in_ms: int) -> datetime:
    return datetime.now() + timedelta(milliseconds=interval_in_ms)


def calculate_interval(days: int, hours: int, minutes: int, seconds: int) -> int:
    return 1000 * (seconds + minutes * 60 + hours * 3600 + days * 86400)


def get_articles(target_type: str, target_value: str) -> list[tuple[str, str, str]]:
    if target_type == task_target.article:
        result = []
        articles = target_value.splitlines()
        for article in articles:
            name, src = wb_service.get_name_and_img_by_article(article)
            result.append((article, name, src))
        return result
    else:
        return []


def calculate_endtime(interval_in_ms: int, amount_of_articles: int, ) -> datetime:
    return datetime.now() + timedelta(interval_in_ms * amount_of_articles)
