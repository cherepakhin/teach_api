import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.employee_group.employee_group_view import EmployeeGroupView


class EmployeeGroupViewTest(BaseTestDB):

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_employees')
  def test_get(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 1
    response = EmployeeGroupView(context, request).get()
    self.assertEqual(response.get('n'), 1)
    self.assertEqual(response.get('name'), 'admins')
    # self.assertEqual(response.get('rights'), [{
    #     'n': 1,
    #     'section': 'question',
    #     'access': 'edit',
    # }])

  @pytest.mark.usefixtures('fix_employees')
  def test_delete(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 1
    response = EmployeeGroupView(context, request).delete()
    self.assertEqual(response, {'status': 'success'})

  @pytest.mark.usefixtures('fix_employees')
  def test_update(self):
    request = testing.DummyRequest(json_body={'name': 'NEW_NAME'})
    context = testing.DummyResource()
    context.n = 1
    response = EmployeeGroupView(context, request).update()
    self.assertEqual(response.get('name'), 'NEW_NAME')
