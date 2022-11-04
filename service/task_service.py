import logging
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from model import task_target, task_status, task_group_status
from model.task import TaskVO
from model.task_group import TaskGroupRq, TaskGroupVO, TaskGroupRs
from service import wb_service

log = logging.getLogger(__name__)


def add_task_group(rq: TaskGroupRq, session: Session, background_tasks: BackgroundTasks) -> TaskGroupRs:
    interval_in_ms = calculate_interval(rq.days, rq.hours, rq.minutes, rq.seconds)

    vo = TaskGroupVO(
        task_type=rq.task_type,
        target_type=rq.target_type,
        target_value=rq.target_value,
        amount=rq.amount,
        interval=interval_in_ms,
        days=rq.days,
        hours=rq.hours,
        minutes=rq.minutes,
        seconds=rq.seconds,
        status=task_group_status.preparing,
        start_datetime=datetime.now(),
        end_datetime=datetime.now() + timedelta(milliseconds=interval_in_ms * rq.amount)
    )

    session.add(vo)
    session.commit()
    session.refresh(vo)

    background_tasks.add_task(add_tasks, rq, task_group_id=vo.id, session=session)

    rs = TaskGroupRs(
        id=vo.id,
        task_type=rq.task_type,
        target_type=rq.target_type,
        amount=rq.amount,
        current_amount=0,
        status=task_group_status.preparing,
        days=rq.days,
        hours=rq.hours,
        minutes=rq.minutes,
        seconds=rq.seconds,
        start_datetime=vo.start_datetime
    )
    log.info(rs)
    log.info("hello world")
    return rs


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
            max_amount=rq.amount,
            interval_in_ms=interval_in_ms,
            next_check_date=calculate_next_check_date(interval_in_ms),
            status=task_status.scheduled,
            task_group_id=task_group_id
        )
        session.add(task_vo)
    task_group_vo = session.query(TaskGroupVO).filter(TaskGroupVO.id == task_group_id).first()
    task_group_vo.status = task_group_status.running
    task_group_vo.max_amount = len(xs)
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
    elif target_type == task_target.brand:
        return wb_service.get_name_and_img_by_brand(target_value)
    elif target_type == task_target.shop:
        return wb_service.get_name_and_img_by_shop(target_value)
