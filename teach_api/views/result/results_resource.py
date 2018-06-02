from pyramid.security import Allow, ALL_PERMISSIONS
import pyramid.httpexceptions as exc
from teach_api.views.login.security import RESULT_EDITOR

acl = [(Allow, RESULT_EDITOR, ALL_PERMISSIONS), ]


class ResultResource(object):

  def __init__(self, n):
    self.n = n

  @property
  def __acl__(self):
    return acl


class ResultsActionResource(dict):

  def __init__(self, action):
    self.action = action

  @property
  def __acl__(self):
    return acl


class ResultsResource(object):

  def __init__(self):
    self.n = 0

  @property
  def __acl__(self):
    return acl

  def __getitem__(self, param):
    if str(param).isdigit():
      try:
        return ResultResource(param)
      except Exception:
        return exc.HTTPNotFound()
    if len(str(param)) > 0:
      try:
        return ResultsActionResource(param)
      except Exception:
        return exc.HTTPNotFound()
