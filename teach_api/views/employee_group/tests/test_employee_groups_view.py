import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.employee_group.employee_groups_view import EmployeeGroupsView


class EmployeeGroupsViewTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_employees')
  def test_create(self):
    request = testing.DummyRequest(json_body={'name': 'NAME1'})
    context = testing.DummyResource()
    response = EmployeeGroupsView(context, request).post()
    self.assertEqual(response.get('n'), 2)
    self.assertEqual(response.get('name'), 'NAME1')
    # self.assertEqual(response.get('rights'), [])
