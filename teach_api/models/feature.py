from datetime import date
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    Index,
    Table,
    ForeignKey,
    Date,
)
from sqlalchemy.orm import relationship
from pyramid_sqlalchemy import BaseObject
from .a_entity import AEntity


association_table = Table('feature_group_to_feature', BaseObject.metadata,
                          Column('feature_n', Integer,
                                 ForeignKey('feature.n')),
                          Column('feature_group_n', Integer,
                                 ForeignKey('feature_group.n')),
                          )


class Feature(BaseObject, AEntity):
  """
  Характеристика
  """
  __tablename__ = 'feature'
  n = Column(Integer, primary_key=True)
  name = Column(Unicode(150), default='')
  # Техническое описание
  info = Column(Unicode(1024), default='')
  # Описание для покупателя
  info_profit = Column(Unicode(1024), default='')
  feature_group = relationship(
      'FeatureGroup',
      secondary=association_table)
  # Кто изменил
  employee_n = Column(Integer, ForeignKey(
      'employee.n', ondelete='CASCADE'), default=1)
  employee = relationship('Employee')
  # Дата изменения
  ddate = Column(Date(), default=date.today)

  __mapper_args__ = {
      "order_by": name
  }

Index('feature_name_idx', Feature.name)
