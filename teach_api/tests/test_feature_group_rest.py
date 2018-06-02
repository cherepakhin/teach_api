import pytest
import json
from pyramid_sqlalchemy import Session

from teach_api.models import FeatureGroup
from .atest_mdt import AViewTest


class FeatureGroupRestTest(AViewTest):

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_feature_group_get(self):
    res = self.testapp.get('/v1/feature_group/1/',
                           headers=self.headers, status=200)
    self.assertEqual(res.json.get('n'), 1)
    # print(res.json)
    self.assertEqual(res.json.get('name'), 'group1')

  # @pytest.mark.skip
  def test_feature_group_delete(self):
    res = self.testapp.delete(
        '/v1/feature_group/1/', headers=self.headers, status=200)
    self.assertEqual(res.json, {'status': 'success'})
    feature_groups = Session.query(FeatureGroup).all()
    assert len(feature_groups) == 0

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_feature_groups')
  def test_feature_group_post(self):
    res = self.testapp.post('/v1/feature_group/1/',
                            json.dumps({'name': 'NEW_NAME'}), headers=self.headers, status=200)
    self.assertEqual(res.json.get('name'), 'NEW_NAME')

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_feature_groups')
  def test_feature_groups_post(self):
    res = self.testapp.post('/v1/feature_group/',
                            json.dumps({'parent_n': 1,
                                        'name': 'NAME',
                                        }), headers=self.headers, status=200)
    # self.assertEqual(res.json, {'n': 1})
    self.assertEqual(res.json.get('n'), 12)
    self.assertEqual(res.json.get('name'), 'NAME')

  @pytest.mark.usefixtures('fix_feature_groups')
  def test_get(self):
    res = self.testapp.get('/v1/feature_group/', params={'name': 'group1'},
                           headers=self.headers, status=200)
    self.assertEqual(len(res.json), 2)

    res = self.testapp.get('/v1/feature_group/', params={'name': 'group11'},
                           headers=self.headers, status=200)
    self.assertEqual(len(res.json), 1)
    self.assertEqual(res.json[0]['n'], 11)
    self.assertEqual(res.json[0]['name'], 'group11')
