from crypt import crypt
# from simplecrypt import decrypt
from pyramid.view import view_config, view_defaults
from pyramid.interfaces import IAuthenticationPolicy
import pyramid.httpexceptions as exc

# from .security import USERS
from .login_resource import LoginResource
from teach_api.controllers.employee_ctrl import EmployeeCtrl
from teach_api.views.employee.employee_json import EmployeeJSON


@view_defaults(
    route_name='rest',
    renderer='json',
    context=LoginResource
)
class LoginView(object):

  def __init__(self, context, request):
    super(LoginView, self).__init__()
    self.context = context
    self.request = request

  @view_config(request_method='POST')
  def post(self):
    name = self.request.json_body.get('name')
    password = self.request.json_body.get('password')
    # print('----name=%s' % name)
    # print('----password=%s' % password)
    try:
      employee = EmployeeCtrl.find_by_name(name)
      # print('----login=%s' % login)
      # print('----name=%s' % name)
      # print('----password=%s' % employee.password)
      # if employee.password == crypt(password, 'secret service'):
      if employee.password == password:
        policy = self.request.registry.queryUtility(IAuthenticationPolicy)
        token = policy.encode_jwt(
            self.request, claims={'sub': name, 'name': employee.name})
        return {
            'token': 'JWT token="' + token.decode('utf-8') + '"',
            'employee': EmployeeJSON().dump(employee).data
        }
      else:
        return exc.HTTPForbidden()
    except Exception:
      return exc.HTTPForbidden()

    # if employee and password and USERS.get(employee) == password:
    #   policy = self.request.registry.queryUtility(IAuthenticationPolicy)
    #   token = policy.encode_jwt(self.request, claims={'sub': employee})

    #   return {
    #       'token': 'JWT token="' + token.decode('utf-8') + '"'
    #   }
    # else:
    #   return exc.HTTPForbidden()
