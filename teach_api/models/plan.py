from sqlalchemy import (
    Column,
    Integer,
    Index,
    ForeignKey,
    UniqueConstraint,
)

from pyramid_sqlalchemy import BaseObject
from sqlalchemy.orm import relationship
from .a_entity import AEntity


class Plan(BaseObject, AEntity):
  """
  План опроса сотрудника на месяц
  """
  __tablename__ = 'plan'
  n = Column(Integer, primary_key=True)
  # Месяц
  month = Column(Integer, nullable=False)
  # Год
  year = Column(Integer, nullable=False)
  # К-во рабочих смен
  qty_work = Column(Integer, default=0)
  # К-во вопросов на месяц
  qty_question = Column(Integer, default=0)
  # Сотрудник для тестирования
  employee_n = Column(Integer, ForeignKey(
      'employee.n', ondelete='CASCADE'), nullable=False)
  employee = relationship('Employee')

  __table_args__ = (
      UniqueConstraint('year', 'month', 'employee_n'),
  )

  def __repr__(self):
    return "\nn=%s\n\temployee_n=%s\n\tyear=%s\n\tmonth=%s\n\tqty_work=%s\n\tqty_question=%s" % \
        (self.n, self.employee_n, self.year,
         self.month, self.qty_work, self.qty_question)


Index('plan_year_month_idx', Plan.year, Plan.month)
Index('plan_employee_idx', Plan.employee_n)
