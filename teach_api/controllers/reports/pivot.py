from pydash import find
from functools import reduce

from datetime import date
from dateutil.relativedelta import relativedelta

from pyramid_sqlalchemy import Session
from sqlalchemy import func

from teach_api.models import Employee, Result


class PivotReport(object):
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

  def __init__(self, year, month):
    super(PivotReport, self).__init__()
    self.year = year
    self.month = month
    self.start_date = date(self.year, self.month, 1)
    self.end_date = self.start_date + relativedelta(months=1)
    self.for_ok = True

  # def generate_arr_days(self):
  #   """ Генерация массива дней между датами"""
  #   # d = datetime.strptime(self.start_date, '%Y-%m-%d')
  #   # from_date = date.fromtimestamp(d.timestamp())
  #   # d = datetime.strptime(self.end_date, '%Y-%m-%d')
  #   # to_date = date.fromtimestamp(d.timestamp())
  #   arr_days = []
  #   d = self.start_date
  #   while d < self.end_date:
  #     arr_days.append(d)
  #     d = d + timedelta(days=1)
  #   return arr_days

  def _process(self, accum, row):
    # print(a)
    elem = find(accum, {'employee_name': row['employee_name']})
    if elem is None:
      elem = {
          'employee_name': row['employee_name'],
          'results': [
              {
                  'ddate': row['ddate'],
                  'qty_all': 0,
                  'qty_ok': 0
              }
          ],
          'qty_all': 0,
          'qty_ok': 0,
      }
      accum.append(elem)

    elem['qty_all'] = elem['qty_all'] + row['qty']
    if self.for_ok:
      elem['qty_ok'] = elem['qty_ok'] + row['qty']

    day_result = find(elem['results'], {
        'ddate': row['ddate']})
    if day_result is None:
      day_result = {
          'ddate': row['ddate'],
          'qty_all': 0,
          'qty_ok': 0
      }
      elem['results'].append(day_result)

    day_result['qty_all'] = day_result['qty_all'] + row['qty']
    if self.for_ok:
      day_result['qty_ok'] = day_result['qty_ok'] + row['qty']

    return accum

  def build(self):
    records_ok = self.get_records(True)
    self.for_ok = True
    report = reduce(self._process, records_ok, [])
    records_false = self.get_records(False)
    self.for_ok = False
    report = reduce(self._process, records_false, report)
    return report

  def get_records(self, isOk):
    q = Session.query(Employee.name, Result.ddate, func.count()).join(
        Result.employee)
    q = q.filter(Result.ddate >= self.start_date, Result.ddate < self.end_date)
    q = q.filter(Result.is_correct == isOk)
    records = q.group_by(Employee.name, Result.ddate).order_by(
        Employee.name, Result.ddate).all()
    named_records = [
        dict(zip(['employee_name', 'ddate', 'qty'], r)) for r in records]

    return named_records
