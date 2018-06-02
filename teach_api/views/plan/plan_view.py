from pyramid.view import view_config, view_defaults
from .plans_resource import PlanResource
from teach_api.models import Plan
from .plan_json import PlanJSON
from teach_api.views.a_entity_view import AEntityView
from teach_api.controllers.plan_ctrl import PlanCtrl


@view_defaults(
    route_name='rest',
    renderer='json',
    context=PlanResource
)
class PlanView(AEntityView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = PlanJSON()
    self.entity = Plan

  @view_config(request_method='GET', permission='edit')
  def get(self):
    return super().get()

  @view_config(request_method='DELETE', permission='edit')
  def delete(self):
    return super().delete()

  @view_config(request_method='POST', permission='edit')
  def update(self):
    return self.serializator.dump(PlanCtrl.update_qty(self.context.n, self.request.json_body)).data
