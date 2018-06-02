from pyramid.view import view_config, view_defaults
from .right_resource import RightsResource
from teach_api.models import Right
from .right_json import RightJSON
from teach_api.views.a_entities_view import AEntitiesView


@view_defaults(
    route_name='rest',
    renderer='json',
    context=RightsResource
)
class RightsView(AEntitiesView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = RightJSON()
    self.entity = Right

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
