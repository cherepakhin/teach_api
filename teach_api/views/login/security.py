import json
from functools import wraps
from pyramid.compat import text_
from pyramid.interfaces import IAuthenticationPolicy
import logging
from teach_api.controllers.employee_ctrl import EmployeeCtrl

EMPLOYEE_EDITOR = 'employee_edit'
EMPLOYEE_VIEWER = 'employee_view'
DEPARTMENT_EDITOR = 'department_edit'

FEATURE_EDITOR = 'feature_edit'
FEATURE_VIEWER = 'feature_view'

QUESTION_EDITOR = 'question_edit'
QUESTION_VIEWER = 'question_view'

RESULT_EDITOR = 'result_edit'
PLAN_EDITOR = 'plan_edit'


def groupfinder_in_db(name, request):
  """Для реального применения"""
  # print('----name=%s' % name)
  # logging.getLogger(__name__).warning('----name=%s' % (name,))
  employee = EmployeeCtrl.find_by_name(name)
  rules = []
  for r in employee.employee_group.rights:
    rules.append(r.rule)
  # print(rules)
  return rules


def get_employee_name(request):
  policy = request.registry.queryUtility(IAuthenticationPolicy)
  if policy:
    jwt_claims = policy.get_claims(request)
    if jwt_claims and 'name' in jwt_claims:
      return jwt_claims['name']
  return ''


def add_employee_name(func):
  """ Декоратор для вставки запрос имени пользователя """
  @wraps(func)
  def wrapper(self, *args, **kwargs):
    # Добавляю в params имя пользователя
    if get_employee_name(self.request) != '':
      js = json.loads(text_(self.request.body, self.request.charset))
      js['employee_name'] = get_employee_name(self.request)
      js['employee_n'] = EmployeeCtrl.find_by_name(js['employee_name']).n
      self.request.body = str.encode(json.dumps(js))
    return func(self, *args, **kwargs)
  return wrapper
