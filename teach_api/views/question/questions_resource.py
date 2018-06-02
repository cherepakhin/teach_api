from pyramid.security import Allow, ALL_PERMISSIONS
import pyramid.httpexceptions as exc
from teach_api.views.login.security import QUESTION_EDITOR, QUESTION_VIEWER

acl = [(Allow, QUESTION_EDITOR, ALL_PERMISSIONS), ]


class QuestionResource(object):

  def __init__(self, n):
    self.n = n

  @property
  def __acl__(self):
    return acl


class QuestionActionResource(dict):

  def __init__(self, action):
    self.action = action

  @property
  def __acl__(self):
    return [(Allow, QUESTION_VIEWER, ALL_PERMISSIONS), ]
    # return acl


class QuestionsResource(object):

  def __init__(self):
    self.n = 0

  @property
  def __acl__(self):
    return acl

  def __getitem__(self, param):
    if str(param).isdigit():
      try:
        return QuestionResource(param)
      except Exception:
        return exc.HTTPNotFound()
    if len(str(param)) > 0:
      try:
        return QuestionActionResource(param)
      except Exception:
        return exc.HTTPNotFound()
