from pyramid.view import view_config, view_defaults
from .feature_groups_resource import FeatureGroupResource
from teach_api.models import FeatureGroup
from .feature_group_json import FeatureGroupFullJSON
from teach_api.views.a_entity_view import AEntityView
from teach_api.controllers.feature_group_ctrl import FeatureGroupCtrl
from teach_api.util.message_json import MessageJSON


@view_defaults(
    route_name='rest',
    renderer='json',
    context=FeatureGroupResource
)
class FeatureGroupView(AEntityView):

  def __init__(self, context, request):
    super().__init__(context, request)
    self.serializator = FeatureGroupFullJSON()
    self.entity = FeatureGroup

  @view_config(request_method='GET', permission='edit')
  def get(self):
    return super().get()

  @view_config(request_method='DELETE', permission='edit')
  def delete(self):
    try:
      FeatureGroupCtrl.delete(self.context.n)
    except Exception as e:
      error_message = 'Error delete feature_group n={}. Error: {}'.format(
          self.context.n, e)
      self.log.warning(error_message)
      return MessageJSON('Error delete feature_group n=%s. Exception: %s' % (self.context.n, e))
    return {'status': 'success'}

  @view_config(request_method='POST', permission='edit')
  def update(self):
    params = self.request.json_body
    if 'name' in params:
      feature_group = FeatureGroupCtrl.update(self.context.n, params['name'])
      return FeatureGroupFullJSON().dump(feature_group).data
    else:
      error_message = 'Error update feature_group n={}. Empty name.'.format(
          self.context.n)
      self.log.warning(error_message)
      return MessageJSON('Error update feature_group n=%s.Empty name.' % (self.context.n))
