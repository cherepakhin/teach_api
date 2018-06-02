from pyramid.view import view_config, view_defaults
from teach_api.models import Result, Question
from .result_json import ResultJSON
from teach_api.views.result.result_json import ResultWithFeatureJSON
from teach_api.views.a_entity_view import AEntityView
from teach_api.controllers.result_ctrl import ResultCtrl
from teach_api.views.result.results_resource import ResultsActionResource
from teach_api.views.login.security import add_employee_name


@view_defaults(
    route_name='rest',
    renderer='json',
    context=ResultsActionResource
)
class ResultActionView(AEntityView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = ResultJSON()
    self.entity = Result

  @add_employee_name
  @view_config(request_method='POST', permission='edit')
  def post(self):
    if self.context.action == 'exam':
      params = self.request.json_body
      res = ResultCtrl.exam(params['question_n'], params[
          'answer_n'], params['employee_name'])
      # print(res.is_correct)
      question = Question.get(params['question_n'])
      feature = question.feature

      return ResultWithFeatureJSON().dump(
          {'feature': feature, 'is_correct': res.is_correct}
      ).data
