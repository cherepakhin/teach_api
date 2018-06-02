from sqlalchemy import (
    Column,
    Integer,
    Unicode,
)

from pyramid_sqlalchemy import BaseObject
from .a_entity import AEntity


class EmployeeGroup(BaseObject, AEntity):
  """
  Группа пользователя
  """
  __tablename__ = 'employee_group'
  n = Column(Integer, primary_key=True)
  name = Column(Unicode(150), default='')

  __mapper_args__ = {
      "order_by": (name,)
  }
