from pyramid.security import Allow, ALL_PERMISSIONS
import pyramid.httpexceptions as exc
from teach_api.views.login.security import PLAN_EDITOR

acl = [(Allow, PLAN_EDITOR, ALL_PERMISSIONS), ]


class PlansMonthResource(object):
  """
  Планы сотрудников на месяц
  Запросы вида plan/2017/12
  """

  def __init__(self, year, month):
    self.year = year
    self.month = month

  @property
  def __acl__(self):
    return acl


class PlanResource(object):

  def __init__(self, n):
    self.n = n

  @property
  def __acl__(self):
    return acl

  def __getitem__(self, n):
    if str(n).isdigit():
      try:
        return PlansMonthResource(self.n, n)
      except Exception:
        return exc.HTTPNotFound()


class PlansResource(object):

  def __init__(self):
    self.n = 0

  @property
  def __acl__(self):
    return acl

  def __getitem__(self, n):
    if str(n).isdigit():
      try:
        return PlanResource(n)
      except Exception:
        return exc.HTTPNotFound()
