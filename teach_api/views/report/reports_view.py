from pyramid.view import view_config, view_defaults
from .reports_resource import ReportResource
# import json
import logging
from teach_api.views.a_entities_view import AEntitiesView
from teach_api.controllers.report_ctrl import ReportCtrl
from teach_api.util.message_json import MessageJSON
from teach_api.views.result.result_json import ResultEmployeeDetailJSON, \
    PivotJSON, \
    PivotCreateFeatureJSON


@view_defaults(
    route_name='rest',
    renderer='json',
    context=ReportResource
)
class ReportsView(AEntitiesView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.log = logging.getLogger(__name__)

  @view_config(request_method='GET', permission='edit')
  def get(self):
    params = self.request.params
    if self.context.name_report == 'employee_feature_group':
      try:
        year = int(params['year'])
        # print(year)
        month = int(params['month'])
        # print(month)
        report = ReportCtrl.employee_feature_group(year, month)
        # return json.dumps(report)
        return report
      except Exception as e:
        error_message = 'Ошибка при создании отчета employee_feature_group: {}'.format(
            e,)
        self.log.error(error_message)
        return MessageJSON(error_message)
    if self.context.name_report == 'employee_detail':
      try:
        year = int(params['year'])
        # print(year)
        month = int(params['month'])
        # print(month)
        employee_name = params['employee_name']
        report = ReportCtrl.employee_detail(employee_name, year, month)
        # print(report)
        # return json.dumps(report)
        return ResultEmployeeDetailJSON().dump(report, many=True).data
      except Exception as e:
        error_message = 'Ошибка при создании отчета employee_detail: {}'.format(
            e,)
        self.log.error(error_message)
        return MessageJSON(error_message)
    if self.context.name_report == 'pivot':
      try:
        year = int(params['year'])
        month = int(params['month'])
        report = ReportCtrl.pivot(year, month)
        # print(report)
        # return json.dumps(report)
        return PivotJSON().dump(report, many=True).data
      except Exception as e:
        error_message = 'Ошибка при создании отчета pivot: {}'.format(
            e,)
        self.log.error(error_message)
        return MessageJSON(error_message)
    if self.context.name_report == 'pivot_create_feature':
      try:
        year = int(params['year'])
        month = int(params['month'])
        report = ReportCtrl.pivot_create_feature_report(year, month)
        return PivotCreateFeatureJSON().dump(report, many=True).data
      except Exception as e:
        error_message = 'Ошибка при создании отчета pivot_create_feature: {}'.format(
            e,)
        self.log.error(error_message)
        return MessageJSON(error_message)
    return MessageJSON('Не задано название отчета')
