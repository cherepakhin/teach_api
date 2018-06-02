from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from pydash import group_by, map_, sorted_uniq, find, order_by
from sqlalchemy import and_
from pyramid_sqlalchemy import Session
from teach_api.controllers.employee_ctrl import EmployeeCtrl
from teach_api.models import Question, Result


class ResultCtrl(object):

  def __init__(self, arg):
    super(ResultCtrl, self).__init__()

  @staticmethod
  def exam(question_n, answer_n, employee_name):
    """
    Проверка ответа на вопрос и сохранение результата тестирования
    """
    result = Result()
    employee = EmployeeCtrl.find_by_name(employee_name)
    result.employee_n = employee.n
    result.question_n = question_n
    result.answer_n = answer_n
    question = Question.get(question_n)
    result.is_correct = (question.answer_n == int(answer_n))
    Session.add(result)
    Session.flush()
    return result

  @staticmethod
  def generate_arr_days(start_date, end_date):
    """ Генерация массива дней между датами"""
    d = datetime.strptime(start_date, '%Y-%m-%d')
    from_date = date.fromtimestamp(d.timestamp())
    d = datetime.strptime(end_date, '%Y-%m-%d')
    to_date = date.fromtimestamp(d.timestamp())
    if from_date > to_date:
      d = from_date
      from_date = to_date
      end_date = d
    arr_days = []
    d = from_date
    while d <= to_date:
      arr_days.append(d)
      d = d + timedelta(days=1)
    return arr_days

  @staticmethod
  def buildReport(start_date, end_date, department):
    """ Формирование СПЕЦИАЛЬНОГО отчета по результатам тестирования
        за период в виде
        [
            {
                employee_name
                results: [
                    {
                        n,
                        ddate,
                        is_correct,
                    }
                ]
            }
        ]
    """
    d = datetime.strptime(start_date, '%Y-%m-%d')
    from_date = date.fromtimestamp(d.timestamp())
    d = datetime.strptime(end_date, '%Y-%m-%d')
    to_date = date.fromtimestamp(d.timestamp())
    # print(start_date)
    # print(end_date)
    # q = Session.query(Result)
    q = Session.query(Result).filter(Result.ddate >= from_date)
    q = q.filter(Result.ddate <= to_date)

    if department != '':
      q = q.filter(Result.employee.department.name == department)
    results = q.all()
    pivot = ResultCtrl.convert_to_pivot(start_date, end_date, results)
    return pivot

  @staticmethod
  def fill_empty_day_in_result(start_date, end_date, results):
    """ Заполнение пустых дней (дни в которые не было ответов)"""
    arr_days = ResultCtrl.generate_arr_days(start_date, end_date)
    for empl_results in results:
      for day in arr_days:
        result = find(empl_results['results'], lambda x: x.ddate == day)
        if result is None:
          empl_results['results'].append(Result(is_correct=False, ddate=day))
      empl_results['results'] = order_by(empl_results['results'], ['ddate'])
    return results

  @staticmethod
  def convert_to_pivot(start_date, end_date, results):
    """ Конвертация в сводную форму """
    g = group_by(results, 'employee.name')
    names = sorted_uniq(map_(results, 'employee.name'))
    list_result = list(
        map(lambda name: {'employee_name': name, 'results': g[name]}, names))
    print(list_result)
    list_result = ResultCtrl.fill_empty_day_in_result(
        start_date, end_date, list_result)
    return list_result

  @staticmethod
  def count_answered(employee, year, month):
    """
    Сотрудником отвечено вопросов год/месяц
    """
    start_date = date(year, month, 1)
    end_date = start_date + relativedelta(months=1)
    # print('{} {}'.format(start_date, end_date))
    # test = Session.query(Result).filter(Result.employee_n == employee.n,
    #                                     Result.ddate >= start_date,
    #                                     Result.ddate < end_date).all()
    # print()
    ret = Session.query(Result).filter(and_(Result.employee_n == employee.n,
                                            Result.ddate >= start_date,
                                            Result.ddate < end_date)).count()
    return ret

  @staticmethod
  def find(params):
    q = Session.query(Result)
    if 'employee_n' in params:
      q = q.filter(Result.employee_n == params['employee_n'])
    if 'date' in params:
      q = q.filter(Result.ddate == params['date'])
    results = q.all()
    return results
