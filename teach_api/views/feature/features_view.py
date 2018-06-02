from pyramid.view import view_config, view_defaults
from .features_resource import FeaturesResource
from teach_api.models import Feature
from .feature_json import FeatureShortJSON, FeatureFullJSON
from .feature_json import FeatureFullWithResultsJSON, FeatureShortWithResultsJSON
from teach_api.views.a_entities_view import AEntitiesView
from teach_api.controllers.feature_ctrl import FeatureCtrl
from teach_api.views.login.security import add_employee_name


@view_defaults(
    route_name='rest',
    renderer='json',
    context=FeaturesResource
)
class FeaturesView(AEntitiesView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = FeatureShortJSON()
    self.entity = Feature

  @view_config(request_method='GET', permission='view')
  def get(self):
    """
    Поиск по:
    имени (name)
    """
    params = {}
    if 'name' in self.request.params:
      params['name'] = self.request.params['name']
    results = FeatureCtrl.find(self.request.params)
    # print(features)
    # return self.serializator.dump(results).data
    return self.get_format(self.request.params).dump(results).data

  def get_format(self, params):
    json_format = FeatureShortWithResultsJSON()
    if 'format' in params:
      if params['format'] == 'full':
        json_format = FeatureFullWithResultsJSON()
    return json_format

  @add_employee_name
  @view_config(request_method='POST', permission='edit')
  def post(self):
    feature = FeatureCtrl.create(self.request.json_body)
    return FeatureFullJSON().dump(feature).data
