from datetime import datetime
from pyramid.view import view_config, view_defaults
from teach_api.models import Result, Question
from teach_api.views.result.result_json import ResultWithFeatureJSON
from teach_api.views.a_entity_view import AEntityView
from teach_api.controllers.result_ctrl import ResultCtrl
from teach_api.views.result.results_resource import ResultsActionResource
from teach_api.views.login.security import add_employee_name
from .result_json import ResultJSON


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
      print('-------------------------')
      print(params['time_begin'])
      time_begin = datetime.strptime(params['time_begin'],'%Y-%m-%d %H:%M:%S')
      time_end = datetime.strptime(params['time_end'],'%Y-%m-%d %H:%M:%S')
      res = ResultCtrl.exam(params['question_n'], params[
          'answer_n'], params['employee_name'],time_begin,time_end)
      # print(res.is_correct)
      question = Question.get(params['question_n'])
      feature = question.feature

      return ResultWithFeatureJSON().dump(
          {'feature': feature, 'is_correct': res.is_correct}
      ).data
