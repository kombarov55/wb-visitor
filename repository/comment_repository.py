from sqlalchemy.orm import Session, load_only

from model.comment import CommentVO


def get_all(session: Session) -> list[str]:
    return session.query(CommentVO).all()


def save(session: Session, comments: list[str]):
    for comment in comments:
        vo = CommentVO(value=comment)
        session.add(vo)
    session.commit()


def delete_all(session: Session):
    session.query(CommentVO).delete()
    session.commit()
