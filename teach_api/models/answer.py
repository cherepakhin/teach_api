from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    ForeignKey,
)

from pyramid_sqlalchemy import BaseObject
from sqlalchemy.orm import relationship, backref
from .a_entity import AEntity


class Answer(BaseObject, AEntity):
  """
  Ответ
  """
  __tablename__ = 'answer'
  n = Column(Integer, primary_key=True)
  question_n = Column(Integer, ForeignKey(
      'question.n', ondelete='CASCADE'), default=1)
  question = relationship('Question', backref=backref(
      'answers', cascade='all, delete-orphan'))
  txt = Column(Unicode(1024), default='')

  def __str__(self):
    return "n=%s txt=%s question_n=%s" % (self.n, self.txt, self.question_n)
