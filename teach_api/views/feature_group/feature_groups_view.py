from pyramid.view import view_config, view_defaults
from .feature_groups_resource import FeatureGroupsResource
from teach_api.models import FeatureGroup
from teach_api.controllers.feature_group_ctrl import FeatureGroupCtrl
from .feature_group_json import FeatureGroupFullJSON
from teach_api.views.a_entities_view import AEntitiesView


@view_defaults(
    route_name='rest',
    renderer='json',
    context=FeatureGroupsResource
)
class FeatureGroupsView(AEntitiesView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = FeatureGroupFullJSON()
    self.entity = FeatureGroup

  @view_config(request_method='GET', permission='edit')
  def get(self):
    """
    Поиск по:
    имени (name)
    """
    if 'name' in self.request.params:
      feature_groups = FeatureGroupCtrl.find_by_like_name(
          name=self.request.params['name'])
      return self.serializator.dump(feature_groups, many=True).data
    else:
      raise Exception('Empty NAME in params for FIND FeatureGroup.')

  @view_config(request_method='POST', permission='edit')
  def post(self):
    params = self.request.json_body
    if 'name' not in params or params['name'] == '':
      raise Exception('Empty NAME in params for create FeatureGroup.')
    parent_n = None
    if 'parent_n' in params:
      parent_n = params['parent_n']
    feature_group = FeatureGroupCtrl.create(parent_n, params['name'])
    # print(feature_group.name)
    return self.serializator.dump(feature_group).data
