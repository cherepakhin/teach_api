from datetime import date, datetime, timedelta
from sqlalchemy import (
    Column,
    Integer,
    Index,
    ForeignKey,
    Date,
    DateTime,
    Boolean,
)

from pyramid_sqlalchemy import BaseObject
from sqlalchemy.orm import relationship
from .a_entity import AEntity


class Result(BaseObject, AEntity):
  """
  Результат опроса
  """
  __tablename__ = 'result'
  n = Column(Integer, primary_key=True)
  question_n = Column(Integer, ForeignKey(
      'question.n', ondelete='CASCADE'), default=1)
  question = relationship('Question')
  answer_n = Column(Integer, ForeignKey(
      'answer.n', ondelete='CASCADE'), default=1)
  answer = relationship('Answer')
  employee_n = Column(Integer, ForeignKey(
      'employee.n', ondelete='CASCADE'), default=1)
  employee = relationship('Employee')
  is_correct = Column(Boolean, default=False)
  ddate = Column(Date, default=date.today)
  # Время начала ответа
  time_begin = Column(DateTime, default=datetime.now)
  # Время окончания ответа
  time_end = Column(DateTime, default=datetime.now)

  # Продолжительность ответа
  @property
  def duration(self):
    sec=self.time_end-self.time_begin
    return str(timedelta(seconds=sec.seconds))

  def __repr__(self):
    return "\nn=%s\n\tquestion_n=%s\n\tanswer_n=%s\n\temployee_n=%s\n\tis_correct=%s\n\tddate=%s" % \
        (self.n, self.question_n, self.answer_n,
         self.employee_n, self.is_correct, self.ddate)


Index('result_question_n_idx', Result.question_n)
Index('result_employee_n_idx', Result.employee_n)
Index('result_ddate_idx', Result.ddate)
