from pyramid.security import Allow, ALL_PERMISSIONS
import pyramid.httpexceptions as exc
from teach_api.views.login.security import RESULT_EDITOR

acl = [(Allow, RESULT_EDITOR, ALL_PERMISSIONS), ]


class ReportResource(object):

  def __init__(self, name_report):
    self.name_report = name_report

  @property
  def __acl__(self):
    return acl


class ReportsResource(object):

  def __init__(self):
    self.name_report = ''

  @property
  def __acl__(self):
    return acl

  def __getitem__(self, name_report):
    if len(str(name_report)) > 0:
      try:
        return ReportResource(name_report)
      except Exception:
        return exc.HTTPNotFound()
    return exc.HTTPNotFound()
