from pyramid.view import view_config, view_defaults
from .questions_resource import QuestionActionResource
from .question_json import QuestionJSON
from teach_api.views.a_entity_view import AEntityView
from teach_api.models import Question
from teach_api.views.login.security import add_employee_name
from teach_api.controllers.question_ctrl import QuestionCtrl


@view_defaults(
    route_name='rest',
    renderer='json',
    context=QuestionActionResource
)
class QuestionActionView(AEntityView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = QuestionJSON()
    self.entity = Question

  @add_employee_name
  @view_config(request_method='POST', permission='view')
  def post(self):
    if self.context.action == 'get_next':
      params = self.request.json_body
      question = QuestionCtrl.generate_question(params['employee_name'])
      return QuestionJSON().dump(question).data
