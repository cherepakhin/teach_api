import logging
from pyramid.view import view_config, view_defaults
from .plans_resource import PlansMonthResource
from teach_api.util.message_json import MessageJSON
from teach_api.models import Plan
from .plan_json import PlanJSON
from teach_api.views.a_entities_view import AEntitiesView
from teach_api.controllers.plan_ctrl import PlanCtrl


@view_defaults(
    route_name='rest',
    renderer='json',
    context=PlansMonthResource
)
class PlansMonthView(AEntitiesView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = PlanJSON()
    self.entity = Plan
    self.log = logging.getLogger(__name__)

  @view_config(request_method='GET', permission='edit')
  def get(self):
    """
    Получение планов на год/месяц
    """
    plans = PlanCtrl.get_on_month(self.context.year, self.context.month)
    return self.serializator.dump(plans, many=True).data

  @view_config(request_method='DELETE', permission='edit')
  def delete(self):
    """
    Удаление планов на год/месяц
    """
    print(self.context.year, self.context.month)
    try:
      PlanCtrl.delete_month(self.context.year, self.context.month)
    except Exception as e:
      error_message = 'Error delete year={} month={}. Error: {}'.format(
          self.context.year, self.context.month, e)
      self.log.warning(error_message)
      return MessageJSON(error_message)
    return {'status': 'success'}
