from pyramid.view import view_config, view_defaults
from .plans_resource import PlansResource
from teach_api.models import Plan
from .plan_json import PlanJSON
from teach_api.views.a_entities_view import AEntitiesView


@view_defaults(
    route_name='rest',
    renderer='json',
    context=PlansResource
)
class PlansView(AEntitiesView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = PlanJSON()
    self.entity = Plan

  @view_config(request_method='GET', permission='edit')
  def get(self):
    return super().get(self.request.params)

  @view_config(request_method='POST', permission='edit')
  def post(self):
    return super().create()
