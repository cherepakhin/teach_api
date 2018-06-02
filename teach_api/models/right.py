from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    Index,
    ForeignKey,
)

from pyramid_sqlalchemy import BaseObject, Session
from sqlalchemy.orm import relationship, backref
from .a_entity import AEntity


class Right(BaseObject, AEntity):
  """
  Права пользователя
  """
  __tablename__ = 'right'
  n = Column(Integer, primary_key=True)
  # Раздел системы. (price,doc, ...)
  section = Column(Unicode(150), default='')
  # Правило (edit,view)
  access = Column(Unicode(150), default='')

  employee_group_n = Column(Integer, ForeignKey(
      'employee_group.n', ondelete='CASCADE'), default=1)
  employee_group = relationship('EmployeeGroup', backref=backref(
      'rights', cascade='all, delete-orphan'))

  @property
  def rule(self):
    return '%s_%s' % (self.section, self.access)

  __mapper_args__ = {
      'order_by': (employee_group_n, section, access)
  }

  @staticmethod
  def find(params):
    filter = Session.query(Right)
    if 'employee_group_n' in params:
      filter = filter.filter(Right.employee_group_n ==
                             params['employee_group_n'])
    return filter.all()

Index('right_section_idx', Right.section)
