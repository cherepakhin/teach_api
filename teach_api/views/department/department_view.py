from pyramid.view import view_config, view_defaults
from .departments_resource import DepartmentResource
from teach_api.models import Department
from .department_json import DepartmentJSON
from teach_api.views.a_entity_view import AEntityView


@view_defaults(
    route_name='rest',
    renderer='json',
    context=DepartmentResource
)
class DepartmentView(AEntityView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = DepartmentJSON()
    self.entity = Department

  @view_config(request_method='GET', permission='edit')
  def get(self):
    return super().get()

  @view_config(request_method='DELETE', permission='edit')
  def delete(self):
    return super().delete()

  @view_config(request_method='POST', permission='edit')
  def update(self):
    return super().update()
