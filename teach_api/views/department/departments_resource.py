from pyramid.security import Allow, ALL_PERMISSIONS
import pyramid.httpexceptions as exc
from teach_api.views.login.security import DEPARTMENT_EDITOR

acl = [(Allow, DEPARTMENT_EDITOR, ALL_PERMISSIONS), ]


class DepartmentResource(object):

  def __init__(self, n):
    self.n = n

  @property
  def __acl__(self):
    return acl


class DepartmentsResource(object):

  def __init__(self):
    self.n = 0

  @property
  def __acl__(self):
    return acl

  def __getitem__(self, n):
    if str(n).isdigit():
      try:
        return DepartmentResource(n)
      except Exception:
        return exc.HTTPNotFound()
