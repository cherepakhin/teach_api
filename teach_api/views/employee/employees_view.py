from pyramid.view import view_config, view_defaults
from .employee_resource import EmployeesResource
from teach_api.models import Employee
from .employee_json import EmployeeJSON
from teach_api.views.a_entities_view import AEntitiesView
from teach_api.controllers.employee_ctrl import EmployeeCtrl


@view_defaults(
    route_name='rest',
    renderer='json',
    context=EmployeesResource
)
class EmployeesView(AEntitiesView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = EmployeeJSON()
    self.entity = Employee

  @view_config(request_method='GET', permission='edit')
  def get(self):
    """
    Поиск по:
    имени (name)
    """
    employees = []
    if 'name' in self.request.params:
      employees = EmployeeCtrl.find_by_like_name(self.request.params['name'])
    else:
      employees = EmployeeCtrl.find_by_like_name('')
    return self.serializator.dump(employees, many=True).data

  @view_config(request_method='POST', permission='edit')
  def post(self):
    params = self.request.json_body

    employee = EmployeeCtrl.create(
        params['name'],
        '',
        'password' in params and params['password'] or '',
        'employee_group' in params and params['employee_group']['n'] or '1',
        'department' in params and params['department']['n'] or '1')
    return self.serializator.dump(employee).data
