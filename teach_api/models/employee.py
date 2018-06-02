from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    Index,
    Boolean,
    ForeignKey,
)

from pyramid_sqlalchemy import BaseObject
from sqlalchemy.orm import relationship, backref
from .a_entity import AEntity


class Employee(BaseObject, AEntity):
  """
  Работник
  """
  __tablename__ = 'employee'
  n = Column(Integer, primary_key=True)
  # Полное имя пользователя
  name = Column(Unicode(150), default='')
  password = Column(Unicode(150), default='')
  # Доп. информация (паспорт...)
  info = Column(Unicode(250), default='')
  # Пользователь отключен
  disabled = Column(Boolean(), default=False)

  employee_group_n = Column(Integer, ForeignKey(
      'employee_group.n', ondelete='CASCADE'), default=1)
  # Группа пользователя. Определяются права
  employee_group = relationship('EmployeeGroup', backref=backref(
      'employees', cascade='all, delete-orphan'))

  department_n = Column(Integer, ForeignKey(
      'department.n', ondelete='CASCADE'), default=1)
  # Группа пользователя. Определяются права
  department = relationship('Department', backref=backref(
      'employees', cascade='all, delete-orphan'))

Index('employee_name_idx', Employee.name)
