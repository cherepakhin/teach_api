import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.right.right_view import RightView


class RightViewTest(BaseTestDB):

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_employees')
  def test_get(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 1
    response = RightView(context, request).get()
    self.assertEqual(response, {'n': 1,
                                'section': 'question',
                                'access': 'edit',
                                })

  @pytest.mark.usefixtures('fix_employees')
  def test_delete(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 1
    response = RightView(context, request).delete()
    self.assertEqual(response, {'status': 'success'})

  @pytest.mark.usefixtures('fix_employees')
  def test_update(self):
    request = testing.DummyRequest(
        json_body={'section': 'doc', 'access': 'view'})
    context = testing.DummyResource()
    context.n = 1
    response = RightView(context, request).update()
    self.assertEqual(response, {'n': 1,
                                'section': 'doc',
                                'access': 'view'
                                })
