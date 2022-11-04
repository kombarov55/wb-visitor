import pydantic
from sqlalchemy import Column, Integer, String

from config import database


class CommentVO(database.base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String)


class CommentRq(pydantic.BaseModel):
    text: str
