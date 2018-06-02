from pyramid.view import view_config, view_defaults
from .departments_resource import DepartmentsResource
from teach_api.models import Department
from .department_json import DepartmentJSON
from teach_api.views.a_entities_view import AEntitiesView


@view_defaults(
    route_name='rest',
    renderer='json',
    context=DepartmentsResource
)
class DepartmentsView(AEntitiesView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = DepartmentJSON()
    self.entity = Department

  @view_config(request_method='GET', permission='edit')
  def get(self):
    """
    Поиск по:
    имени (name)
    """
    params = {}
    if 'name' in self.request.params:
      params['name'] = self.request.params['name']
    return super().get(params)

  @view_config(request_method='POST', permission='edit')
  def post(self):
    return super().create()
