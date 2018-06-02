from pyramid.view import view_config, view_defaults
from .var_resource import VarsResource

from teach_api.controllers.var_ctrl import VarCtrl
# from pyshop.controllers.v_ctrl import VarCtrl


@view_defaults(
    route_name='rest',
    renderer='json',
    context=VarsResource
)
class VarView(object):

  def __init__(self, context, request):
    super(VarView, self).__init__()
    # print(request)
    self.context = context
    self.request = request

  @view_config(request_method='GET')
  def get(self):
    return VarCtrl.get_init_var()
