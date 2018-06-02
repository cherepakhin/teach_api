from pyramid_sqlalchemy import Session
from teach_api.controllers.employee_ctrl import EmployeeCtrl
from teach_api.models import (
    Plan,
    Employee,
)


class PlanCtrl(object):
  """
  Контроллер для управления планами вопросов
  """

  def __init__(self, arg):
    super(PlanCtrl, self).__init__()

  @staticmethod
  def create(employee_n, year, month, qty_work=0, qty_question=0):
    """
    Создание плана опроса для сотрудника
    qty_work - к-во смен
    qty_question - задать вопросов в месяц
    """
    params = {
        'employee_n': employee_n,
        'year': year,
        'month': month,
        'qty_work': qty_work,
        'qty_question': qty_question
    }
    plan = Plan.create(params)
    return plan

  @staticmethod
  def create_for_employees(nn_employees, year, month, qty_work=0, qty_question=0):
    """
    Создание планов для списка сотрудников
    nn_employees - num[] - массив номеров сотрудников
    """
    ret = []
    for employee_n in nn_employees:
      plan = PlanCtrl.create(employee_n, year, month, qty_work, qty_question)
      ret.append(plan)
    return ret

  @staticmethod
  def create_on_month(year, month):
    """
    Создание планов на месяц для всех работающих сотрудников
    """
    ret = []
    employees = EmployeeCtrl.find_all_worked()
    # print(len(employees))
    for employee in employees:
      plan = PlanCtrl.create(employee.n, year, month)
      ret.append(plan)
    return ret

  @staticmethod
  def find(params):
    """
    Отбор планов
    Параметры:
    month - num
    year -num
    employee_name - string часть имени сотрудника
    """
    q = Session.query(Plan)
    if 'year' in params:
      q = q.filter(Plan.year == params['year'])
    if 'month' in params:
      q = q.filter(Plan.month == params['month'])
    if 'employee_name' in params:
      q = q.join(Plan.employee).filter(
          Employee.name.ilike('%' + params['employee_name'] + '%'))
    plans = q.all()
    return plans

  @staticmethod
  def update_qty(n, params):
    if 'qty_work' in params:
      Plan.update(n, {'qty_work': params['qty_work']})
    if 'qty_question' in params:
      Plan.update(n, {'qty_question': params['qty_question']})
    return Plan.get(n)

  @staticmethod
  def delete(n):
    Plan.delete(n)

  @staticmethod
  def get_on_month(year, month):
    plans = PlanCtrl.find({'year': year, 'month': month})
    if len(plans) > 0:
      return plans
    else:
      return PlanCtrl.create_on_month(year, month)

  @staticmethod
  def delete_month(year, month):
    # print('delete {} {} {} {}'.format(year, month, type(year), type(int(year))))
    if year > 0 and month > 0:
      Session.query(Plan).filter(Plan.year == year,
                                 Plan.month == month).delete()
      Session.flush()

  @staticmethod
  def get_current_plan(employee_name, year, month):
    """
    Получение плана сотрудника на год/месяц
    """
    plans = PlanCtrl.find({'employee_name': employee_name,
                           'year': year, 'month': month})
    if len(plans) == 0:
      raise Exception('Plan not found for employee={} year={} month={}'.format(
          employee_name, year, month))
    return plans[0]
