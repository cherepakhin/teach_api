from crypt import crypt
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
import pytest
from pyramid_sqlalchemy import Session
from teach_api.models import (
    Feature,
    Question,
    Answer,
    Right,
    Employee,
    EmployeeGroup,
    Result,
    Department,
    FeatureGroup,
    Plan,
)

import warnings
from sqlalchemy.exc import SAWarning

# Silence the warning about Decimal usage with sqlite
warnings.filterwarnings(
    action='ignore', category=SAWarning,
    message=r'.*sqlite\+pysqlite does \*not\* support Decimal objects.*')


today = date(2017, 8, 18)
yesterday = today - timedelta(days=1)


# def pytest_addoption(parser):
#   parser.addoption('--autocommit', action="store", default="True",
#                    help="my option: type1 or type2")


@pytest.fixture(scope='session')
def sqlalchemy_url():
  # return 'sqlite:///:memory:'
  return 'sqlite:///sqltest.sqlite'


@pytest.fixture(scope='session')
def sql_echo():
  # return True
  return False


@pytest.fixture(scope='function')
def fix_employees(request, sql_session):
  Session.add(EmployeeGroup(n=1, name='admins'))
  Session.add(Right(n=1, employee_group_n=1,
                    section='question', access='edit'))
  Session.add(Employee(n=1, name='NAME_1',
                       password='PASSWORD', employee_group_n=1, disabled=False))
  Session.add(Employee(n=2, name='NAME_2',
                       password='PASSWORD', employee_group_n=1, disabled=False))
  # Session.commit()


@pytest.fixture()
def fix_feature_groups(request, sql_session):
  Session.add(FeatureGroup(n=1, name='group1'))
  Session.add(FeatureGroup(n=11, name='group11', parent_n=1))


@pytest.fixture()
def fix_many_feature_groups(request, sql_session):
  Session.add(FeatureGroup(n=1, name='group1'))
  Session.add(FeatureGroup(n=11, name='group11', parent_n=1))
  Session.add(FeatureGroup(n=12, name='group12', parent_n=1))

  Session.add(FeatureGroup(n=2, name='group2'))
  Session.add(FeatureGroup(n=21, name='group21', parent_n=2))
  # Session.flush()


@pytest.fixture(scope='function')
def fix_features(request, sql_session):
  feature_group_1 = FeatureGroup(n=1, name='group1')
  Session.add(feature_group_1)
  feature = Feature(n=1, name='-')
  feature.feature_group.append(feature_group_1)
  Session.add(feature)
  # Session.commit()


@pytest.fixture()
# @pytest.yield_fixture
def fix_questions(request, sql_session):
  Session.add(Feature(n=1, name='-'))
  Session.add(Feature(n=2, name='FEATURE1'))
  Session.add(Feature(n=3, name='FEATURE2'))
  # Session.commit()
  # Вопрос 1 к Теме 2
  Session.add(Question(n=21, feature_n=2, txt='CONTENT21', answer_n=211))
  Session.add(Answer(n=211, question_n=21, txt='CONTENT211'))
  Session.add(Answer(n=212, question_n=21, txt='CONTENT212'))
  Session.add(Answer(n=213, question_n=21, txt='CONTENT213'))

  # Вопрос 2 к Теме 2
  # Session.add(Question(n=22, feature_n=2, txt='CONTENT22', answer_n=211))
  # Session.add(Answer(n=221, question_n=22, txt='CONTENT221'))
  # Session.add(Answer(n=222, question_n=22, txt='CONTENT222'))
  # Session.add(Answer(n=223, question_n=22, txt='CONTENT223'))

  # Вопрос 1 к Теме 3
  # Session.add(Question(n=31, feature_n=3, txt='CONTENT31', answer_n='311'))
  # Session.add(Answer(n=311, question_n=31, txt='CONTENT311'))
  # Session.add(Answer(n=312, question_n=31, txt='CONTENT312'))
  # Session.add(Answer(n=313, question_n=31, txt='CONTENT313'))

  # Вопрос 2 к Теме 3
  # Session.add(Question(n=32, feature_n=3, txt='CONTENT32', answer_n='321'))
  # Session.add(Answer(n=321, question_n=32, txt='CONTENT321'))
  # Session.add(Answer(n=322, question_n=32, txt='CONTENT322'))
  # Session.add(Answer(n=323, question_n=32, txt='CONTENT323'))
  # Session.commit()
  # Session.commit()


@pytest.fixture()
def fix_disabled_employees(request, sql_session):
  Session.add(EmployeeGroup(n=1, name='admins'))
  Session.add(Employee(n=1,  name='NAME',
                       password='PASSWORD', employee_group_n=1, disabled=True))


# @pytest.mark.usefixtures('fix_questions')
# @pytest.mark.usefixtures('fix_employees')
@pytest.fixture()
def fix_results(request, sql_session):
  Session.add(EmployeeGroup(n=1, name='admins'))
  Session.add(Employee(n=1,  name='NAME',
                       password='PASSWORD', employee_group_n=1, disabled=False))

  Session.add(Feature(n=1, name='-'))
  Session.add(Feature(n=2, name='FEATURE1'))
  Session.add(Feature(n=3, name='FEATURE2'))
  # Session.commit()
  # Вопрос 1 к Теме 2
  Session.add(Question(n=21, feature_n=2, txt='CONTENT21', answer_n=211))
  Session.add(Answer(n=211, question_n=21, txt='CONTENT211'))
  Session.add(Answer(n=212, question_n=21, txt='CONTENT212'))
  Session.add(Answer(n=213, question_n=21, txt='CONTENT213'))

  # Вопрос 2 к Теме 2
  Session.add(Question(n=22, feature_n=2, txt='CONTENT22', answer_n=211))
  Session.add(Answer(n=221, question_n=22, txt='CONTENT221'))
  Session.add(Answer(n=222, question_n=22, txt='CONTENT222'))
  Session.add(Answer(n=223, question_n=22, txt='CONTENT223'))

  # Вопрос 1 к Теме 3
  Session.add(Question(n=31, feature_n=3, txt='CONTENT31', answer_n='311'))
  Session.add(Answer(n=311, question_n=31, txt='CONTENT311'))
  Session.add(Answer(n=312, question_n=31, txt='CONTENT312'))
  Session.add(Answer(n=313, question_n=31, txt='CONTENT313'))

  Session.add(Result(n=1, question_n=21, answer_n=211,
                     is_correct=True, employee_n=1))
  Session.add(Result(n=2, question_n=22, answer_n=221,
                     is_correct=False, employee_n=1))


@pytest.fixture()
def fix_results_for_rest(request, sql_session):
  Session.add(Feature(n=1, name='-'))
  Session.add(Feature(n=2, name='FEATURE1'))
  Session.add(Feature(n=3, name='FEATURE2'))
  # Session.commit()
  # Вопрос 1 к Теме 2
  Session.add(Question(n=21, feature_n=2, txt='CONTENT21', answer_n=211))
  # Session.commit()
  Session.add(Answer(n=211, question_n=21, txt='CONTENT211'))
  Session.add(Answer(n=212, question_n=21, txt='CONTENT212'))
  Session.add(Answer(n=213, question_n=21, txt='CONTENT213'))

  # Вопрос 2 к Теме 2
  Session.add(Question(n=22, feature_n=2, txt='CONTENT22', answer_n=211))
  # Session.commit()
  Session.add(Answer(n=221, question_n=22, txt='CONTENT221'))
  Session.add(Answer(n=222, question_n=22, txt='CONTENT222'))
  Session.add(Answer(n=223, question_n=22, txt='CONTENT223'))
  # Session.commit()

  # Вопрос 1 к Теме 3
  Session.add(Question(n=31, feature_n=3, txt='CONTENT31', answer_n='311'))
  # Session.commit()
  Session.add(Answer(n=311, question_n=31, txt='CONTENT311'))
  Session.add(Answer(n=312, question_n=31, txt='CONTENT312'))
  Session.add(Answer(n=313, question_n=31, txt='CONTENT313'))
  # Session.commit()

  Session.add(Result(n=1, question_n=21, answer_n=211,
                     is_correct=True, employee_n=1, ddate=yesterday))
  Session.add(Result(n=2, question_n=22, answer_n=221,
                     is_correct=False, employee_n=1, ddate=yesterday))
  # Session.commit()


@pytest.fixture()
def fix_employees_for_test(request, sql_session):
  Session.add(EmployeeGroup(n=1, name='admins'))
  Session.add(Right(n=1, employee_group_n=1,
                    section='employee', access='edit'))
  Session.add(Right(n=3, employee_group_n=1,
                    section='question', access='edit'))
  Session.add(Right(n=4, employee_group_n=1,
                    section='answer', access='edit'))
  Session.add(Right(n=5, employee_group_n=1,
                    section='result', access='edit'))
  Session.add(Right(n=6, employee_group_n=1,
                    section='feature', access='edit'))
  Session.add(Right(n=7, employee_group_n=1,
                    section='department', access='edit'))
  Session.add(Right(n=8, employee_group_n=1,
                    section='plan', access='edit'))
  # Session.add(Employee(n=1,  name='NAME', password=crypt(
  #     'password', 'secret service'), employee_group_n=1))
  Session.add(Employee(n=1,  name='NAME',
                       password='password', employee_group_n=1))


@pytest.fixture(scope='function')
def fix_departments(request, sql_session):
  Session.add(Department(n=1, name='-'))


@pytest.fixture(scope='function')
def fix_many_features(request, sql_session):
  for x in range(15):
    name = 'FEATURE {}'.format(x)
    Session.add(Feature(n=x, name=name))


@pytest.fixture()
def fix_full_fixteres(request, sql_session):
  Session.add(FeatureGroup(n=1, name='group1'))
  feature_group = FeatureGroup(n=11, name='group11', parent_n=1)
  Session.add(feature_group)

  feature = Feature(n=1, name='FEATURE_1',
                    info='INFO_1', info_profit='INFO_PROFIT_1', feature_group=[feature_group, ])

  Session.add(feature)
  Session.add(Question(n=1, feature_n=1, txt='QUESTION_1', answer_n=2))

  Session.add(Answer(n=1, question_n=1, txt='ANSWER_1'))
  Session.add(Answer(n=2, question_n=1, txt='ANSWER_2'))
  Session.add(Answer(n=3, question_n=1, txt='ANSWER_3'))


@pytest.fixture()
def fix_report(request, sql_session):
  Session.add(EmployeeGroup(n=1, name='admins'))
  Session.add(Employee(n=1,  name='NAME_1',
                       employee_group_n=1, disabled=False))
  # Этот тупой. Нет правильных ответов
  Session.add(Employee(n=2,  name='NAME_2',
                       employee_group_n=1, disabled=False))

  Session.add(Feature(n=1, name='FEATURE_1'))
  Session.add(Feature(n=2, name='FEATURE_2'))

  Session.add(Question(n=1, feature_n=1, txt='QUESTION_1', answer_n=12))
  Session.add(Answer(n=11, question_n=1, txt='ANSWER_11'))
  Session.add(Answer(n=12, question_n=1, txt='ANSWER_12'))

  Session.add(Question(n=2, feature_n=2, txt='QUESTION_2', answer_n=21))
  Session.add(Answer(n=21, question_n=2, txt='ANSWER_21'))
  Session.add(Answer(n=22, question_n=2, txt='ANSWER_22'))

  Session.add(Result(n=11, question_n=1, answer_n=12,
                     is_correct=True, employee_n=1, ddate=date.today()))
  Session.add(Result(n=12, question_n=1, answer_n=11,
                     is_correct=False, employee_n=2, ddate=date.today()))

  Session.add(Result(n=21, question_n=2, answer_n=21,
                     is_correct=True, employee_n=1, ddate=date.today() + timedelta(days=1)))
  Session.add(Result(n=22, question_n=2, answer_n=22,
                     is_correct=False, employee_n=2, ddate=date.today() + timedelta(days=1)))


@pytest.fixture(scope='function')
def fix_employees_for_plan(request, sql_session):
  Session.add(EmployeeGroup(n=1, name='SELLERS'))
  Session.add(Right(n=1, employee_group_n=1,
                    section='question', access='edit'))
  Session.add(Employee(n=1, name='EMPLOYEE1',
                       password='', employee_group_n=1, disabled=False))
  Session.add(Employee(n=2, name='EMPLOYEE2',
                       password='', employee_group_n=1, disabled=False))
  Session.add(Employee(n=3, name='EMPLOYEE_DISABLED',
                       password='', employee_group_n=1, disabled=True))


@pytest.fixture(scope='function')
def fix_plan(request, sql_session):
  Session.add(Plan(n=1, employee_n=1, year=2017,
                   month=12, qty_work=1, qty_question=1))


@pytest.fixture()
def fix_results_for_generate(request, sql_session):
  feature_group_1 = FeatureGroup(n=1, name='GROUP_1', parent_n=1)
  Session.add(feature_group_1)
  feature_group_2 = FeatureGroup(n=2, name='GROUP_2', parent_n=1)
  Session.add(feature_group_2)

  Session.add(Feature(n=1, name='-'))
  Session.add(Feature(n=2, name='FEATURE1', feature_group=[feature_group_1, ]))
  Session.add(Feature(n=3, name='FEATURE2', feature_group=[feature_group_2, ]))
  # Session.commit()
  # Вопрос 1 к Теме 2
  Session.add(Question(n=21, feature_n=1, txt='CONTENT21', answer_n=211))
  # Session.commit()
  Session.add(Answer(n=211, question_n=21, txt='CONTENT211'))
  Session.add(Answer(n=212, question_n=21, txt='CONTENT212'))
  Session.add(Answer(n=213, question_n=21, txt='CONTENT213'))

  # Вопрос 2 к Теме 2
  Session.add(Question(n=22, feature_n=2, txt='CONTENT22', answer_n=211))
  # Session.commit()
  Session.add(Answer(n=221, question_n=22, txt='CONTENT221'))
  Session.add(Answer(n=222, question_n=22, txt='CONTENT222'))
  Session.add(Answer(n=223, question_n=22, txt='CONTENT223'))
  # Session.commit()

  # Вопрос 1 к Теме 3
  Session.add(Question(n=31, feature_n=3, txt='CONTENT31', answer_n='311'))
  # Session.commit()
  Session.add(Answer(n=311, question_n=31, txt='CONTENT311'))
  Session.add(Answer(n=312, question_n=31, txt='CONTENT312'))
  Session.add(Answer(n=313, question_n=31, txt='CONTENT313'))
  # Session.commit()

  _today = date.today()
  Session.add(Result(n=1, question_n=21, answer_n=211,
                     is_correct=True, employee_n=1, ddate=_today))
  # Session.add(Result(n=2, question_n=22, answer_n=221,
  #                    is_correct=False, employee_n=1, ddate=_today))

  # Session.add(Result(n=3, question_n=22, answer_n=221,
  #                    is_correct=False, employee_n=2, ddate=today))


@pytest.fixture()
def fix_results_for_repeat(request, sql_session):
  feature_group_1 = FeatureGroup(n=1, name='GROUP_1', parent_n=1)
  Session.add(feature_group_1)

  Session.add(Feature(n=1, name='FEATURE_1',
                      feature_group=[feature_group_1, ]))
  # Session.commit()
  # Вопрос 1 к Теме 2
  Session.add(Question(n=21, feature_n=1, txt='CONTENT21', answer_n=211))
  # Session.commit()
  Session.add(Answer(n=211, question_n=21, txt='CONTENT211'))

  Session.add(Question(n=31, feature_n=1, txt='CONTENT31', answer_n='311'))
  # Session.commit()
  Session.add(Answer(n=311, question_n=31, txt='CONTENT311'))
  # Session.commit()

  _today = date.today()
  Session.add(Result(n=10, question_n=21, answer_n=211,
                     is_correct=True, employee_n=1, ddate=_today))
  Session.add(Result(n=11, question_n=21, answer_n=211,
                     is_correct=True, employee_n=1, ddate=_today))
  Session.add(Result(n=30, question_n=31, answer_n=221,
                     is_correct=False, employee_n=1, ddate=today))


@pytest.fixture()
def fix_for_employee_feature_group(request, sql_session):
  feature_group_1 = FeatureGroup(n=1, name='GROUP_1', parent_n=1)
  Session.add(feature_group_1)
  feature_group_2 = FeatureGroup(n=2, name='GROUP_2', parent_n=1)
  Session.add(feature_group_2)

  Session.add(Feature(n=1, name='-'))
  Session.add(Feature(n=2, name='FEATURE_1',
                      feature_group=[feature_group_1, ]))
  Session.add(Feature(n=3, name='FEATURE_2',
                      feature_group=[feature_group_2, ]))

  Session.add(Question(n=21, feature_n=1, txt='CONTENT_21'))
  Session.add(Question(n=22, feature_n=2, txt='CONTENT_22'))
  Session.add(Question(n=31, feature_n=3, txt='CONTENT_31'))

  _today = date.today()
  Session.add(Result(n=1, question_n=21,
                     is_correct=True, employee_n=1, ddate=_today))
  Session.add(Result(n=2, question_n=22,
                     is_correct=False, employee_n=1, ddate=_today))

  Session.add(Result(n=3, question_n=22,
                     is_correct=True, employee_n=2, ddate=_today))
  Session.add(Result(n=4, question_n=31,
                     is_correct=False, employee_n=2, ddate=_today))
  Session.add(Plan(n=1, employee_n=1, year=date.today().year,
                   month=date.today().month, qty_work=1, qty_question=1))
  Session.add(Plan(n=2, employee_n=2, year=date.today().year,
                   month=date.today().month, qty_work=1, qty_question=2))


@pytest.fixture()
def fix_results_for_pivot_report(request, sql_session):

  feature_group_1 = FeatureGroup(n=1, name='GROUP_1', parent_n=1)
  Session.add(feature_group_1)

  Session.add(Feature(n=1, name='FEATURE_1',
                      feature_group=[feature_group_1, ]))
  # Session.commit()
  # Вопрос 1 к Теме 2
  Session.add(Question(n=21, feature_n=1, txt='CONTENT21', answer_n=211))
  # Session.commit()
  Session.add(Answer(n=211, question_n=21, txt='CONTENT211'))

  Session.add(Question(n=31, feature_n=1, txt='CONTENT31', answer_n='311'))
  # Session.commit()
  Session.add(Answer(n=311, question_n=31, txt='CONTENT311'))
  # Session.commit()

  _today = date.today()
  tomorrow = _today + relativedelta(days=1)
  Session.add(Result(n=10, question_n=21, answer_n=211,
                     is_correct=True, employee_n=1, ddate=_today))
  Session.add(Result(n=11, question_n=21, answer_n=211,
                     is_correct=True, employee_n=1, ddate=_today))
  Session.add(Result(n=12, question_n=31, answer_n=221,
                     is_correct=False, employee_n=1, ddate=_today))

  Session.add(Result(n=13, question_n=21, answer_n=211,
                     is_correct=True, employee_n=1, ddate=tomorrow))
  Session.add(Result(n=14, question_n=31, answer_n=221,
                     is_correct=False, employee_n=1, ddate=tomorrow))


@pytest.fixture()
def fix_for_pivot_create_feature_report(request, sql_session):
  Session.add(EmployeeGroup(n=2, name='SELLERS'))
  Session.add(Right(n=2, employee_group_n=1,
                    section='question', access='edit'))
  Session.add(Employee(n=2, name='EMPLOYEE_1',
                       password='', employee_group_n=2, disabled=False))
  Session.add(Employee(n=3, name='EMPLOYEE_2',
                       password='', employee_group_n=2, disabled=False))

  feature_group_1 = FeatureGroup(n=1, name='GROUP_1', parent_n=1)
  Session.add(feature_group_1)

  Session.add(Feature(n=1, name='FEATURE_11',
                      feature_group=[feature_group_1, ], employee_n=2, ddate=date.today()))
  Session.add(Feature(n=2, name='FEATURE_12',
                      feature_group=[feature_group_1, ], employee_n=2, ddate=date.today() + timedelta(days=1)))
  Session.add(Feature(n=3, name='FEATURE_21',
                      feature_group=[feature_group_1, ], employee_n=3, ddate=date.today()))
  Session.add(Feature(n=4, name='FEATURE_22',
                      feature_group=[feature_group_1, ], employee_n=3, ddate=date.today() + timedelta(days=1)))
