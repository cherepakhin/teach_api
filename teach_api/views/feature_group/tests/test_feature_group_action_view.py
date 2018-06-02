import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.feature_group.feature_group_action_view import FeatureGroupActionView


class FeatureGroupTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_get_root(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.action = 'root'
    response = FeatureGroupActionView(context, request).get()

    # print(response)
    self.assertEqual(len(response), 1)
    self.assertEqual(response[0]['n'], 1)
    self.assertEqual(response[0]['name'], 'group1')
    self.assertEqual(len(response[0]['children']), 1)
