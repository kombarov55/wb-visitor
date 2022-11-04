from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from config import database
from model.task_group import TaskGroupRq, TaskGroupRs, TaskGroupShortRs
from repository import task_group_repository
from service import task_service


def get_session():
    db = database.session_local()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.post("/task_group")
async def post_task_group(rq: TaskGroupRq, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    return task_service.add_task_group(rq, session, background_tasks)


@router.get("/task_group", response_model=list[TaskGroupRs])
async def get_task_group(offset: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return task_group_repository.find_task_groups(session, offset, limit)


@router.get("/task_group/short", response_model=list[TaskGroupShortRs])
async def get_task_group_short(offset: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return task_group_repository.find_task_groups_short(session, offset, limit)


@router.get("/task_group/{task_group_id}", response_model=TaskGroupRs)
async def get_task_group_by_id(task_group_id: int, session: Session = Depends(get_session)):
    return task_group_repository.find_task_group_by_id(session, task_group_id)
