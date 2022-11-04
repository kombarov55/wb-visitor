from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import database
from model.comment import CommentRq
from repository import comment_repository


def get_session():
    db = database.session_local()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.post("/comments")
def set_comments(rq: CommentRq, session: Session = Depends(get_session)):
    comments = rq.text.splitlines()
    comment_repository.delete_all(session)
    comment_repository.save(session, comments)


@router.get("/comments")
def get_comments(session: Session = Depends(get_session)) -> list[str]:
    vo_list = comment_repository.get_all(session)
    return list(map(lambda v: v.value, vo_list))
