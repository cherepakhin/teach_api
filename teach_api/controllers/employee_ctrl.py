from pyramid_sqlalchemy import Session
from teach_api.models import Employee, Right, EmployeeGroup


class EmployeeCtrl(object):
  """Контроллер для пользователей"""

  def __init__(self, arg):
    super(EmployeeCtrl, self).__init__()
    self.arg = arg

  @staticmethod
  def find_by_name(name):
    q = Session.query(Employee).filter(
        Employee.name == name, Employee.disabled.is_(False))
    employees = q.all()
    if len(employees) == 1:
      return employees[0]
    else:
      raise Exception('Employee not found.')

  @staticmethod
  def find_all_worked():
    """
    Получение всех работающих сотрудников
    () -> employee[]
    """
    q = Session.query(Employee).filter(Employee.disabled.is_(False))
    employees = q.all()
    return employees

  @staticmethod
  def find_by_like_name(name):
    q = Session.query(Employee)

    q = q.filter(Employee.name.ilike('%' + name + '%'))
    employees = q.all()
    return employees

  @staticmethod
  def create(name, info, password, employee_group_n, department_n):
    params = {
        'name': name,
        'password': password,
        'info': info,
        'employee_group_n': employee_group_n,
        'department_n': department_n
    }
    employee = Employee.create(params)
    return employee

  @staticmethod
  def update(n, name, info, password, employee_group_n, department_n):
    params = {
        'name': name,
        'password': password,
        'info': info,
        'employee_group_n': employee_group_n,
        'department_n': department_n
    }
    if len(params['password']) == 0:
      del params['password']
    employee = Employee.update(n, params)
    return employee

  @staticmethod
  def create_employee_group(name):
    params = {
        'name': name,
    }
    employee_group = EmployeeGroup.create(params)
    return employee_group

  @staticmethod
  def add_right_to_employee_group(employee_group_n, section, access):
    params = {
        'employee_group_n': employee_group_n,
        'section': section,
        'access': access
    }
    Right.create(params)
    q = Session.query(EmployeeGroup).filter(
        EmployeeGroup.n == employee_group_n)
    employees = q.all()
    return employees[0]

  @staticmethod
  def delete_right(right_n):
    right = Right.get(right_n)
    employee_group_n = right.employee_group_n
    Right.delete(right_n)
    q = Session.query(EmployeeGroup).filter(
        EmployeeGroup.n == employee_group_n)
    employee_groups = q.all()
    return employee_groups[0]
