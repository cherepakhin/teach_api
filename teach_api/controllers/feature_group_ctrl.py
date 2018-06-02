from pyramid_sqlalchemy import Session
from teach_api.models import FeatureGroup


class FeatureGroupCtrl(object):
  """Контроллер для групп хар-к"""

  def __init__(self, arg):
    super(FeatureGroupCtrl, self).__init__()
    self.arg = arg

  @staticmethod
  def find_by_name(name):
    q = Session.query(FeatureGroup).filter(
        FeatureGroup.name == name)
    feature_groups = q.all()
    if len(feature_groups) == 1:
      return feature_groups[0]
    else:
      raise Exception('FeatureGroup not found.')

  @staticmethod
  def find_by_like_name(name):
    q = Session.query(FeatureGroup)

    q = q.filter(FeatureGroup.name.ilike('%' + name + '%'))
    feature_groups = q.all()
    return feature_groups

  @staticmethod
  def create(parent_n, name):
    if parent_n is not None and parent_n < 0:
      parent_n = None
    feature_group = FeatureGroup.create({'name': name, 'parent_n': parent_n})
    return feature_group

  @staticmethod
  def delete(n):
    Session.query(FeatureGroup).filter(FeatureGroup.parent_n == n).delete()
    FeatureGroup.delete(n)

  @staticmethod
  def update(n, name):
    feature_group = FeatureGroup.update(n, {'name': name})
    return feature_group

  @staticmethod
  def get_root():
    q = Session.query(FeatureGroup).filter(FeatureGroup.parent_n == None)
    feature_groups = q.all()
    # for f in feature_groups:
    #   print('feature {}'.format(f.name))
    return feature_groups
