from pydash import find
from functools import reduce
from pyramid_sqlalchemy import Session
from sqlalchemy import func
from datetime import date
from dateutil.relativedelta import relativedelta
from teach_api.models import Result, Employee, Question, Feature, FeatureGroup
from teach_api.controllers.plan_ctrl import PlanCtrl


class EmployeeFeatureGroupReport(object):
  """
  Генератор отчета со структурой:
  [
    {
      'employee_name': 'EMPLOYEE_NAME',
     'feature_groups': [
         {'name': 'FEATURE_GROUP_1',
          'qty_all': 4, 'qty_ok': 2},

         {'name': 'FEATURE_GROUP_2',
          'qty_all': 2, 'qty_ok': 1}
     ],
     'qty_all': 6,
     'qty_ok': 3,
     'qty_plan': 5
     },
     ....
  ]

  rowsOk, rowsFalse - ряды с правильными и неправильными ответами
  Вид рядов:
        {
            'employee_name': 'EMPLOYEE_1',
            'feature_group': 'FEATURE_GROUP_1',
            'qty': 1
        },
  """

  # флаг какие ряды обрабатываются.
  # True - с правильными ответами,
  # False - с неправильными
  for_ok = True

  def __init__(self, year, month):
    super(EmployeeFeatureGroupReport, self).__init__()
    self.year = year
    self.month = month

  def _process(self, a, row):
    # print(a)
    elem = find(a, {'employee_name': row['employee_name']})
    if elem is None:
      elem = {
          'employee_name': row['employee_name'],
          'feature_groups': [
              {
                  'name': row['feature_group'],
                  'qty_all': 0,
                  'qty_ok': 0
              }
          ],
          'qty_all': 0,
          'qty_ok': 0,
          'qty_plan': 0
      }
      a.append(elem)

    elem['qty_all'] = elem['qty_all'] + row['qty']
    if self.for_ok:
      elem['qty_ok'] = elem['qty_ok'] + row['qty']

    feature_group = find(elem['feature_groups'], {
                         'name': row['feature_group']})
    if feature_group is None:
      feature_group = {
          'name': row['feature_group'],
          'qty_all': 0,
          'qty_ok': 0
      }
      elem['feature_groups'].append(feature_group)

    feature_group['qty_all'] = feature_group['qty_all'] + row['qty']
    if self.for_ok:
      feature_group['qty_ok'] = feature_group['qty_ok'] + row['qty']

    return a

  def append_plans(self, report):
    """
    Добавить плановое по к-во вопросов в отчет
    """
    plans = PlanCtrl.get_on_month(self.year, self.month)
    for r in report:
      plan = find(plans, lambda p: p.employee.name == r['employee_name'])
      if plan is not None:
        r['qty_plan'] = plan.qty_question
    return report

  def build(self):
    self.for_ok = True
    rowsOk = self.get_records(self.for_ok)
    report = reduce(self._process, rowsOk, [])

    self.for_ok = False
    rowsFalse = self.get_records(self.for_ok)
    report = reduce(self._process, rowsFalse, report)

    report = self.append_plans(report)

    return report

# select e.name,g.name,count(is_correct)
# from result r left outer join employee e on r.employee_n=e.n
# left outer join question q on r.question_n=q.n
# left outer join feature_group_to_feature fg on q.feature_n=fg.feature_n
# left outer join feature_group g on fg.feature_group_n=g.n
# group by e.name,g.name
# order by e.name,g.name

  def get_records(self, isOk):
    start_date = date(self.year, self.month, 1)
    end_date = start_date + relativedelta(months=1)
    q = Session.query(Employee.name, FeatureGroup.name, func.count()).join(
        Result.employee).join(
        Result.question).join(
        Question.feature).outerjoin(
        Feature.feature_group)
    q = q.filter(Result.ddate >= start_date, Result.ddate < end_date)
    q = q.filter(Result.is_correct == isOk)
    records = q.group_by(Employee.name, FeatureGroup.name).order_by(
        Employee.name, FeatureGroup.name).all()
    # .namedtuple()
    # records = Session.query(Employee.name).all()
    named_records = [
        dict(zip(['employee_name', 'feature_group', 'qty'], r)) for r in records]
    return named_records
