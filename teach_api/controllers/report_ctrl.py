from datetime import date
from dateutil.relativedelta import relativedelta
from pyramid_sqlalchemy import Session

from teach_api.models import Result, Employee
from teach_api.controllers.reports.employee_feature_group import EmployeeFeatureGroupReport
from teach_api.controllers.reports.pivot import PivotReport
from teach_api.controllers.reports.pivot_create_feature import PivotCreateFeatureReport


class ReportCtrl(object):
  """
  Контроллер отчетов
  """

  def __init__(self, arg):
    super(ReportCtrl, self).__init__()
    self.arg = arg

# select e.name,g.name,count(*)
# from result r,employee e,question q,feature_group g, feature_group_to_feature fg
# where
# r.employee_n=e.n and
# r.question_n=q.n and
# q.feature_n=fg.feature_n and
# fg.feature_group_n=g.n
# group by e.name,g.name
# order by e.name,g.name

# select e.name,g.name,count(is_correct)
# from result r left outer join employee e on r.employee_n=e.n
# left outer join question q on r.question_n=q.n
# left outer join feature_group_to_feature fg on q.feature_n=fg.feature_n
# left outer join feature_group g on fg.feature_group_n=g.n
# group by e.name,g.name
# order by e.name,g.name
  @staticmethod
  def employee_feature_group(year, month):
    """
    Получение отчета со структурой:
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
    """
    report = EmployeeFeatureGroupReport(year, month).build()
    return report

  @staticmethod
  def employee_detail(employee_name, year, month):
    """
    Получение детализации опроса сотрудника
    """
    start_date = date(year, month, 1)
    end_date = start_date + relativedelta(months=1)
    q = Session.query(Result).join(Result.employee).filter(
        Result.ddate >= start_date,
        Result.ddate < end_date,
        Employee.name == employee_name).order_by(Result.ddate)
    results = q.all()
    return results

  @staticmethod
  def pivot(year, month):
    """ Формирование СПЕЦИАЛЬНОГО отчета по результатам тестирования
        за период в виде
        [
            {
                employee_name
                results: [
                    {
                        ddate,    // дата
                        qty_all,  // кол-во заданных вопросов
                        qty_ok,   // кол-во правильных ответов
                    }
                ]
            }
        ]
    """
    return PivotReport(year, month).build()

  @staticmethod
  def pivot_create_feature_report(year, month):
    """ Формирование отчета ввода новых хар-к
        за период в виде
        [
            {
                employee_name
                results: [
                    {
                        ddate,    // дата
                        qtyl,  // кол-во введенных хар-к
                    }
                ]
            }
        ]
    """
    return PivotCreateFeatureReport(year, month).build()
