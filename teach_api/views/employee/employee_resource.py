from pyramid.security import Allow, ALL_PERMISSIONS
import pyramid.httpexceptions as exc
from teach_api.views.login.security import EMPLOYEE_EDITOR

acl = [(Allow, EMPLOYEE_EDITOR, ALL_PERMISSIONS), ]


class EmployeeResource(object):

  def __init__(self, n):
    self.n = n

  @property
  def __acl__(self):
    return acl


class EmployeesResource(object):

  def __init__(self):
    self.n = 0

  @property
  def __acl__(self):
    return acl

  def __getitem__(self, n):
    if str(n).isdigit():
      try:
        return EmployeeResource(n)
      except Exception:
        return exc.HTTPNotFound()
