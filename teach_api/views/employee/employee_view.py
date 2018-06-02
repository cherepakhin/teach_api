from pyramid.view import view_config, view_defaults
from .employee_resource import EmployeeResource
from teach_api.models import Employee
from .employee_json import EmployeeJSON
from teach_api.views.a_entity_view import AEntityView
from teach_api.controllers.employee_ctrl import EmployeeCtrl


@view_defaults(
    route_name='rest',
    renderer='json',
    context=EmployeeResource
)
class EmployeeView(AEntityView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = EmployeeJSON()
    self.entity = Employee

  @view_config(request_method='GET', permission='edit')
  def get(self):
    return super().get()

  @view_config(request_method='DELETE', permission='edit')
  def delete(self):
    return super().delete()

  @view_config(request_method='POST', permission='edit')
  def update(self):
    params = self.request.json_body
    employee = EmployeeCtrl.update(
        self.context.n,
        params['name'],
        '',
        'password' in params and params['password'] or '',
        'employee_group' in params and params['employee_group']['n'] or '1',
        'department' in params and params['department']['n'] or '1')
    return self.serializator.dump(employee).data
