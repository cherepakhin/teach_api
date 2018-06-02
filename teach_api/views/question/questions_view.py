from pyramid.view import view_config, view_defaults
from .questions_resource import QuestionsResource
from teach_api.models import Question
from .question_json import QuestionJSON
from teach_api.views.a_entities_view import AEntitiesView


@view_defaults(
    route_name='rest',
    renderer='json',
    context=QuestionsResource
)
class QuestionsView(AEntitiesView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = QuestionJSON()
    self.entity = Question

  @view_config(request_method='GET', permission='edit')
  def get(self):
    """
    Поиск по:
    имени (name)
    """
    params = {}
    if 'txt' in self.request.params:
      params['txt'] = self.request.params['txt']
    return super().get(params)

  @view_config(request_method='POST', permission='edit')
  def post(self):
    return super().create()
