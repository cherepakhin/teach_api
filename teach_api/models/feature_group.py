from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    ForeignKey,
    Index,
)

from pyramid_sqlalchemy import BaseObject
from .a_entity import AEntity
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property


class FeatureGroup(BaseObject, AEntity):
  """
  Группа хар-ки
  """
  __tablename__ = 'feature_group'
  n = Column(Integer, primary_key=True)
  name = Column(Unicode(150), default='')

  parent_n = Column(Integer, ForeignKey('feature_group.n'))
  children = relationship('FeatureGroup',
                          backref=backref('parent', remote_side=[n])
                          )

  @hybrid_property
  def parent_name(self):
    if self.parent_n is not None:
      return self.parent.name
    else:
      return ''

  __mapper_args__ = {
      "order_by": (name,)
  }

Index('feature_group_name_idx', FeatureGroup.name)
