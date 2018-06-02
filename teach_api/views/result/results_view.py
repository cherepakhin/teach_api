from pyramid.view import view_config, view_defaults
from .results_resource import ResultsResource
from teach_api.models import Result
from .result_json import ResultJSON
from teach_api.views.a_entities_view import AEntitiesView


@view_defaults(
    route_name='rest',
    renderer='json',
    context=ResultsResource
)
class ResultsView(AEntitiesView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = ResultJSON()
    self.entity = Result

  @view_config(request_method='GET', permission='edit')
  def get(self):
    params = self.request.params
    return super().get(params)

  @view_config(request_method='POST', permission='edit')
  def post(self):
    return super().create()
