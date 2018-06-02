from pyramid_sqlalchemy import Session

from teach_api.models import (
    Employee,
    EmployeeGroup,
    Department
)
from teach_api.views.employee.employee_json import EmployeeJSON
from teach_api.views.employee_group.employee_group_json import EmployeeGroupJSON
from teach_api.views.department.department_json import DepartmentJSON
from teach_api.controllers.feature_group_ctrl import FeatureGroupCtrl
from teach_api.views.feature_group.feature_group_json import FeatureGroupFullJSON


class VarCtrl(object):

  def __init__(self, arg):
    super(VarCtrl, self).__init__()

  @staticmethod
  def get_init_var():
    """
    Получение структуры
    начальных значений для загрузки системы
    """
    employees = EmployeeJSON().dump(Session.query(Employee).all(), many=True).data
    employee_groups = EmployeeGroupJSON().dump(
        Session.query(EmployeeGroup).all(), many=True).data
    departments = DepartmentJSON().dump(
        Session.query(Department).all(), many=True).data
    feature_groups = FeatureGroupFullJSON().dump(
        FeatureGroupCtrl.get_root(), many=True).data
    return {
        'employees': employees,
        'employee_groups': employee_groups,
        'departments': departments,
        'feature_groups': feature_groups,
    }
