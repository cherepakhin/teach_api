import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.feature_group.feature_groups_view import FeatureGroupsView


class FeatureGroupsViewTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_create(self):
    request = testing.DummyRequest(json_body={'parent_n': 1, 'name': 'NAME1'})
    context = testing.DummyResource()
    response = FeatureGroupsView(context, request).post()
    self.assertEqual(response['n'], 12)
    self.assertEqual(response['name'], 'NAME1')
    self.assertEqual(response['parent_n'], 1)

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_create_except_for_empty_name(self):
    request = testing.DummyRequest(json_body={'parent_n': 1, 'name': ''})
    context = testing.DummyResource()
    with pytest.raises(Exception) as e:
      FeatureGroupsView(context, request).post()
    assert 'Empty NAME in params for create FeatureGroup.' in str(e.value)

    request = testing.DummyRequest(json_body={'parent_n': 1})
    context = testing.DummyResource()
    with pytest.raises(Exception) as e:
      FeatureGroupsView(context, request).post()
    assert 'Empty NAME in params for create FeatureGroup.' in str(e.value)

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_create_for_none_parent(self):
    request = testing.DummyRequest(json_body={'name': 'NAME1'})
    context = testing.DummyResource()
    response = FeatureGroupsView(context, request).post()
    self.assertEqual(response['n'], 12)
    self.assertEqual(response['name'], 'NAME1')
    self.assertEqual(response['parent_n'], None)

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_get(self):
    request = testing.DummyRequest(params={'name': 'group'})
    context = testing.DummyResource()
    response = FeatureGroupsView(context, request).get()
    self.assertEqual(len(response), 2)

    request = testing.DummyRequest(params={'name': 'group11'})
    context = testing.DummyResource()
    response = FeatureGroupsView(context, request).get()
    self.assertEqual(len(response), 1)
    self.assertEqual(response[0]['name'], 'group11')
