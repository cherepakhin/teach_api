from pyramid.security import Allow, ALL_PERMISSIONS
import pyramid.httpexceptions as exc
from teach_api.views.login.security import FEATURE_EDITOR, FEATURE_VIEWER

acl = [(Allow, FEATURE_EDITOR, ALL_PERMISSIONS),
       (Allow, FEATURE_VIEWER, 'view'),
       ]


class FeatureGroupResource(object):

  def __init__(self, n):
    self.n = n

  @property
  def __acl__(self):
    return acl


class FeatureGroupsActionResource(dict):

  def __init__(self, action):
    self.action = action

  @property
  def __acl__(self):
    return acl


class FeatureGroupsResource(object):

  def __init__(self):
    self.n = 0

  @property
  def __acl__(self):
    return acl

  def __getitem__(self, param):
    if str(param).isdigit():
      try:
        return FeatureGroupResource(param)
      except Exception:
        return exc.HTTPNotFound()
    if len(str(param)) > 0:
      try:
        return FeatureGroupsActionResource(param)
      except Exception:
        return exc.HTTPNotFound()
