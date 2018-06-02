import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.right.rights_view import RightsView


class RightsViewTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_employees')
  def test_create(self):
    request = testing.DummyRequest(
        json_body={'employee_group_n': 1, 'section': 'doc', 'access': 'view'})
    context = testing.DummyResource()
    response = RightsView(context, request).post()
    self.assertEqual(response, {'n': 2,
                                'section': 'doc',
                                'access': 'view',
                                })
