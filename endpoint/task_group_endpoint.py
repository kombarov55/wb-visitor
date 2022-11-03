from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from config import database
from model.task_group import TaskGroupRq, TaskGroupRs
from repository import task_group_repository
from service import task_service


def get_session():
    db = database.session_local()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.post("/task_group", response_model=TaskGroupRs)
async def post_task_group(rq: TaskGroupRq, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    return task_service.add_task_group(rq, session, background_tasks)


@router.get("/task_group", response_model=list[TaskGroupRs])
async def get_task_group(offset: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return task_group_repository.find_task_groups(session, offset, limit)
