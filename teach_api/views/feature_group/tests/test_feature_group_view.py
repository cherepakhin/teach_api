import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.feature_group.feature_group_view import FeatureGroupView


class FeatureGroupViewTest(BaseTestDB):

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_feature_groups')
  def test_get(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 1
    response = FeatureGroupView(context, request).get()
    self.assertEqual(response.get('n'), 1)
    self.assertEqual(response.get('name'), 'group1')
    self.assertEqual(len(response.get('children')), 1)
    self.assertEqual(response.get('parent_name'), '')

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_get_children(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 11
    response = FeatureGroupView(context, request).get()
    self.assertEqual(response.get('n'), 11)
    self.assertEqual(response.get('name'), 'group11')
    self.assertEqual(len(response.get('children')), 0)
    self.assertEqual(response.get('parent_name'), 'group1')

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_delete(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 1
    response = FeatureGroupView(context, request).delete()
    self.assertEqual(response, {'status': 'success'})

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_update(self):
    request = testing.DummyRequest(json_body={'name': 'NEW_NAME'})
    context = testing.DummyResource()
    context.n = 1
    response = FeatureGroupView(context, request).update()
    self.assertEqual(response.get('n'), 1)
    self.assertEqual(response.get('name'), 'NEW_NAME')
