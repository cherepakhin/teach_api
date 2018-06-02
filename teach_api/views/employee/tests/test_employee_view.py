import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.employee.employee_view import EmployeeView


class EmployeeViewTest(BaseTestDB):

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_employees')
  def test_get(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 1
    response = EmployeeView(context, request).get()
    self.assertEqual(response.get('n'), 1)
    self.assertEqual(response.get('name'), 'NAME_1')
    self.assertEqual(response['employee_group']['n'], 1)
    self.assertEqual(response['employee_group']['name'], 'admins')
    # self.assertEqual(response['employee_group']['rights'], [{
    #     'n': 1,
    #     'section': 'question',
    #     'access': 'edit'
    # }])

  @pytest.mark.usefixtures('fix_employees')
  def test_delete(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 1
    response = EmployeeView(context, request).delete()
    self.assertEqual(response, {'status': 'success'})

  @pytest.mark.usefixtures('fix_employees')
  def test_update(self):
    request = testing.DummyRequest(json_body={'name': 'NEW_NAME'})
    context = testing.DummyResource()
    context.n = 1
    response = EmployeeView(context, request).update()
    self.assertEqual(response.get('n'), 1)
    self.assertEqual(response.get('name'), 'NEW_NAME')
    self.assertEqual(response['employee_group']['n'], 1)
    self.assertEqual(response['employee_group']['name'], 'admins')
    # self.assertEqual(response['employee_group']['rights'], [{
    #     'n': 1,
    #     'section': 'question',
    #     'access': 'edit'
    # }])
