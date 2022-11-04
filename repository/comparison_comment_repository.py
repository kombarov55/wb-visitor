from sqlalchemy.orm import Session

from model.comparison_comment import ComparisonCommentVO


def get_all(session: Session) -> list[str]:
    return session.query(ComparisonCommentVO).all()


def save(session: Session, comments: list[str]):
    for comment in comments:
        vo = ComparisonCommentVO(value=comment)
        session.add(vo)
    session.commit()


def delete_all(session: Session):
    session.query(ComparisonCommentVO).delete()
    session.commit()
