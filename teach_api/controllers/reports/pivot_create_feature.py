from pydash import find
from functools import reduce

from datetime import date
from dateutil.relativedelta import relativedelta

from pyramid_sqlalchemy import Session
from sqlalchemy import func

from teach_api.models import Employee, Feature


class PivotCreateFeatureReport(object):
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

  def __init__(self, year, month):
    super(PivotCreateFeatureReport, self).__init__()
    self.year = year
    self.month = month
    self.start_date = date(self.year, self.month, 1)
    self.end_date = self.start_date + relativedelta(months=1)

  def _process(self, accum, row):
    # print(a)
    elem = find(accum, {'employee_name': row['employee_name']})
    if elem is None:
      elem = {
          'employee_name': row['employee_name'],
          'results': [
              {
                  'ddate': row['ddate'],
                  'qty': 0,
              }
          ],
          'qty': 0,
      }
      accum.append(elem)

    elem['qty'] = elem['qty'] + row['qty']

    day_result = find(elem['results'], {
        'ddate': row['ddate']})
    if day_result is None:
      day_result = {
          'ddate': row['ddate'],
          'qty': 0,
      }
      elem['results'].append(day_result)

    day_result['qty'] = day_result['qty'] + row['qty']

    return accum

  def build(self):
    records = self.get_records()
    report = reduce(self._process, records, [])
    return report

  def get_records(self):
    q = Session.query(Employee.name, Feature.ddate, func.count()).join(
        Feature.employee)
    q = q.filter(Feature.ddate >= self.start_date,
                 Feature.ddate < self.end_date)
    records = q.group_by(Employee.name, Feature.ddate).order_by(
        Employee.name, Feature.ddate).all()
    named_records = [
        dict(zip(['employee_name', 'ddate', 'qty'], r)) for r in records]

    return named_records
