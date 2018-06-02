from pyramid.view import view_config, view_defaults

from teach_api.models import FeatureGroup
from .feature_group_json import FeatureGroupFullJSON
from teach_api.views.a_entity_view import AEntityView
from teach_api.controllers.feature_group_ctrl import FeatureGroupCtrl
from teach_api.views.feature_group.feature_groups_resource import FeatureGroupsActionResource


@view_defaults(
    route_name='rest',
    renderer='json',
    context=FeatureGroupsActionResource
)
class FeatureGroupActionView(AEntityView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = FeatureGroupFullJSON()
    self.entity = FeatureGroup

  @view_config(request_method='GET', permission='view')
  def get(self):
    if self.context.action == 'root':
      feature_groups = FeatureGroupCtrl.get_root()
      return FeatureGroupFullJSON().dump(feature_groups, many=True).data
