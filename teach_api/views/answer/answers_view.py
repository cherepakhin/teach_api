from pyramid.view import view_config, view_defaults
from .answers_resource import AnswersResource
from teach_api.models import Answer
from .answer_json import AnswerJSON
from teach_api.views.a_entities_view import AEntitiesView


@view_defaults(
    route_name='rest',
    renderer='json',
    context=AnswersResource
)
class AnswersView(AEntitiesView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = AnswerJSON()
    self.entity = Answer

  @view_config(request_method='GET', permission='edit')
  def get(self):
    params = self.request.params
    return super().get(params)

  @view_config(request_method='POST', permission='edit')
  def post(self):
    return super().create()
