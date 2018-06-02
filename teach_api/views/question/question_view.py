from pyramid.view import view_config, view_defaults
from .questions_resource import QuestionResource
from teach_api.models import Question
from .question_json import QuestionJSON
from teach_api.views.a_entity_view import AEntityView


@view_defaults(
    route_name='rest',
    renderer='json',
    context=QuestionResource
)
class QuestionView(AEntityView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = QuestionJSON()
    self.entity = Question

  @view_config(request_method='GET', permission='edit')
  def get(self):
    return super().get()

  @view_config(request_method='DELETE', permission='edit')
  def delete(self):
    return super().delete()

  @view_config(request_method='POST', permission='edit')
  def update(self):
    return super().update()
