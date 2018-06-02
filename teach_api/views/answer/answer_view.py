from pyramid.view import view_config, view_defaults
from .answers_resource import AnswerResource
from teach_api.models import Answer
from .answer_json import AnswerJSON
from teach_api.views.a_entity_view import AEntityView


@view_defaults(
    route_name='rest',
    renderer='json',
    context=AnswerResource
)
class AnswerView(AEntityView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = AnswerJSON()
    self.entity = Answer

  @view_config(request_method='GET', permission='edit')
  def get(self):
    return super().get()

  @view_config(request_method='DELETE', permission='edit')
  def delete(self):
    return super().delete()

  @view_config(request_method='POST', permission='edit')
  def update(self):
    return super().update()
