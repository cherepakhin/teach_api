from sqlalchemy import (
    Column,
    Integer,
    Unicode,
)

from pyramid_sqlalchemy import BaseObject, Session
from .a_entity import AEntity


class Department(BaseObject, AEntity):
  """
  Подразделение пользователя
  """
  __tablename__ = 'department'
  n = Column(Integer, primary_key=True)
  name = Column(Unicode(150), default='')

  @staticmethod
  def get_default():
    try:
      defaultDepartment = Department.get(1)
    except Exception:
      defaultDepartment = Department.create({'n': 1, 'name': '-'})
    return defaultDepartment

  @staticmethod
  def find(params):
    filter = Session.query(Department)
    if 'name' in params:
      filter = filter.filter(Department.name.ilike('%' + params['name'] + '%'))
    return filter.all()
