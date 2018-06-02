from pyramid.security import Allow, ALL_PERMISSIONS
import pyramid.httpexceptions as exc
from teach_api.views.login.security import FEATURE_EDITOR, FEATURE_VIEWER

acl = [(Allow, FEATURE_EDITOR, ALL_PERMISSIONS),
       (Allow, FEATURE_VIEWER, 'view'),
       ]


class FeatureResource(object):

  def __init__(self, n):
    self.n = n

  @property
  def __acl__(self):
    return acl


class FeaturesResource(object):

  def __init__(self):
    self.n = 0

  @property
  def __acl__(self):
    return acl

  def __getitem__(self, n):
    if str(n).isdigit():
      try:
        return FeatureResource(n)
      except Exception:
        return exc.HTTPNotFound()
