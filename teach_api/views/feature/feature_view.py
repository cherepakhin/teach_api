from pyramid.view import view_config, view_defaults
from .features_resource import FeatureResource
from teach_api.models import Feature
from .feature_json import FeatureShortJSON, FeatureFullJSON
from teach_api.views.a_entity_view import AEntityView
from teach_api.controllers.feature_ctrl import FeatureCtrl
from teach_api.views.login.security import add_employee_name


@view_defaults(
    route_name='rest',
    renderer='json',
    context=FeatureResource
)
class FeatureView(AEntityView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = FeatureShortJSON()
    self.entity = Feature

  @view_config(request_method='GET', permission='view')
  def get(self):
    return super().get()

  @view_config(request_method='DELETE', permission='edit')
  def delete(self):
    return super().delete()

  @add_employee_name
  @view_config(request_method='POST', permission='edit')
  def update(self):
    feature = FeatureCtrl.update(self.context.n, self.request.json_body)
    return FeatureFullJSON().dump(feature).data
