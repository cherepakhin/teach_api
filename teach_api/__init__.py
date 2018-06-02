from decimal import *
import logging

from pyramid.config import Configurator
from pyramid.response import Response

from pyramid.authorization import ACLAuthorizationPolicy
from teach_api.views.login.login_resource import LoginResource
from teach_api.views.employee_group.employee_group_resource import EmployeeGroupsResource
from teach_api.views.employee.employee_resource import EmployeesResource
from teach_api.views.right.right_resource import RightsResource
from teach_api.views.feature.features_resource import FeaturesResource
from teach_api.views.feature_group.feature_groups_resource import FeatureGroupsResource
from teach_api.views.answer.answers_resource import AnswersResource
from teach_api.views.question.questions_resource import QuestionsResource
from teach_api.views.result.results_resource import ResultsResource
from teach_api.views.department.departments_resource import DepartmentsResource
from teach_api.views.var.var_resource import VarsResource
from teach_api.views.plan.plans_resource import PlansResource
from teach_api.views.report.reports_resource import ReportsResource

# from teach_api.models import (
#     EmployeeGroup,
#     Employee,
#     Right,
#     Question,
#     Answer,
#     Result,
# )


def site(request):
  # pp = pprint.PrettyPrinter(indent=4)
  # print('request=', vars(request))
  # pp.pprint(vars(request))
  # print(request)
  # print(request)
  # print('\n=================SITE')
  # return Response(request.authenticated_userid)
  return Response('OK')


getcontext().prec = 19
getcontext().rounding = ROUND_HALF_UP


def rest_factory(request):
  return {
      'login': LoginResource(),
      'employee_group': EmployeeGroupsResource(),
      'employee': EmployeesResource(),
      'right': RightsResource(),

      'feature': FeaturesResource(),
      'feature_group': FeatureGroupsResource(),
      'answer': AnswersResource(),
      'question': QuestionsResource(),
      'result': ResultsResource(),
      'department': DepartmentsResource(),
      'var': VarsResource(),
      'plan': PlansResource(),
      'report': ReportsResource(),
  }


def configure_route(config):
  config.add_route('home', '/home')
  config.add_view(site, route_name='home')
  config.add_route('rest', '/v1/*traverse', factory=rest_factory)
  config.scan()
  return config


def main(global_config, **settings):
  log = logging.getLogger(__name__)
  log.warning(u'Старт')
  log.warning('++++++++++++++++++++++start')
  # print('++++++++++++++++++++++start')
  config = Configurator(settings=settings)
  # config.include('pyramid_chameleon')
  config.set_authorization_policy(ACLAuthorizationPolicy())
  # config.include('pyramid_tm')
  config.include('pyramid_sqlalchemy')
  config.include('pyramid_jwtauth')

  config = configure_route(config)
  # return config.make_wsgi_app()
  from wsgicors import CORS
  return CORS(config.make_wsgi_app(), headers="*", methods="*", maxage="180", origin="*")
