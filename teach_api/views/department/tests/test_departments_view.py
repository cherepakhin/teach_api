import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.department.departments_view import DepartmentsView


class DepartmentsViewTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_departments')
  def test_create(self):
    request = testing.DummyRequest(json_body={'name': 'NAME1'})
    context = testing.DummyResource()
    response = DepartmentsView(context, request).post()
    self.assertEqual(response['n'], 2)
    self.assertEqual(response['name'], 'NAME1')
