import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.employee.employees_view import EmployeesView


class EmployeesViewTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_employees')
  def test_create(self):
    request = testing.DummyRequest(json_body={'name': 'NAME_3'})
    context = testing.DummyResource()
    response = EmployeesView(context, request).post()
    self.assertEqual(response['n'], 3)
    self.assertEqual(response['name'], 'NAME_3')
    self.assertEqual(response['employee_group']['n'], 1)
    self.assertEqual(response['employee_group']['name'], 'admins')
