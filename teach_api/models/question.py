from datetime import date
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    Index,
    ForeignKey,
    Date,
)

from pyramid_sqlalchemy import BaseObject
from sqlalchemy.orm import relationship, backref
from .a_entity import AEntity


class Question(BaseObject, AEntity):
  """
  Вопрос
  """
  __tablename__ = 'question'
  n = Column(Integer, primary_key=True)
  feature_n = Column(Integer, ForeignKey(
      'feature.n', ondelete='CASCADE'), default=1)
  feature = relationship('Feature', backref=backref(
      'questions', cascade='all, delete-orphan'))
  # Сам вопрос
  txt = Column(Unicode(1024), default='')
  ddate = Column(Date(), default=date.today)
  # Правильный ответ (Answer не присоединяю, т.к.возникает циклическая
  # зависимость)
  answer_n = Column(Integer, default=1)

  def __str__(self):
    return "n=%s feature_n=%s txt=%s ddate=%s answer_n=%s" % (self.n, self.feature_n, self.txt, self.ddate, self.answer_n)

Index('question_content_idx', Question.txt)
