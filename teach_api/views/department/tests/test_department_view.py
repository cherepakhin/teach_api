import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.department.department_view import DepartmentView


class DepartmentViewTest(BaseTestDB):

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_departments')
  def test_get(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 1
    response = DepartmentView(context, request).get()
    self.assertEqual(response.get('n'), 1)
    self.assertEqual(response.get('name'), '-')

  @pytest.mark.usefixtures('fix_departments')
  def test_delete(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 1
    response = DepartmentView(context, request).delete()
    self.assertEqual(response, {'status': 'success'})

  @pytest.mark.usefixtures('fix_departments')
  def test_update(self):
    request = testing.DummyRequest(json_body={'name': 'NEW_NAME'})
    context = testing.DummyResource()
    context.n = 1
    response = DepartmentView(context, request).update()
    self.assertEqual(response.get('n'), 1)
    self.assertEqual(response.get('name'), 'NEW_NAME')
