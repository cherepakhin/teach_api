import pytest
import json
from pyramid_sqlalchemy import Session
from datetime import date
from teach_api.models import Feature
from .atest_mdt import AViewTest


class FeatureRestTest(AViewTest):

  @pytest.mark.usefixtures('fix_features')
  def test_feature_get(self):
    res = self.testapp.get('/v1/feature/1/',
                           headers=self.headers, status=200)
    self.assertEqual(res.json.get('n'), 1)
    # print(res.json)
    self.assertEqual(res.json.get('name'), '-')

  # @pytest.mark.skip
  def test_feature_delete(self):
    res = self.testapp.delete(
        '/v1/feature/1/', headers=self.headers, status=200)
    self.assertEqual(res.json, {'status': 'success'})
    features = Session.query(Feature).all()
    assert len(features) == 0

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_features')
  def test_feature_post(self):
    res = self.testapp.post('/v1/feature/1/',
                            json.dumps({'name': 'NEW_NAME'}), headers=self.headers, status=200)
    self.assertEqual(res.json.get('name'), 'NEW_NAME')
    self.assertEqual(res.json['employee']['n'], 1)
    self.assertEqual(res.json['ddate'], date.today().strftime('%Y-%m-%d'))

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_features')
  def test_features_post(self):
    res = self.testapp.post('/v1/feature/',
                            json.dumps({'n': 0,
                                        'name': 'FEATURE_NAME',
                                        'info': 'FEATURE_INFO',
                                        'info_profit': 'FEATURE_INFO_PROFIT',
                                        'questions': [
                                            {
                                                'n': 0,
                                                'txt': 'QUESTION_TXT',
                                                'answer_n': -1,
                                                'answers': [
                                                    {'n': -1,
                                                     'txt': 'ANSWER_1'},
                                                ],
                                            }
                                        ],
                                        'feature_group': [
                                            {
                                                'n': 1
                                            }
                                        ]
                                        }), headers=self.headers, status=200)
    # self.assertEqual(res.json, {'n': 1})
    self.assertEqual(res.json.get('n'), 2)
    self.assertEqual(res.json.get('name'), 'FEATURE_NAME')
    self.assertEqual(res.json['employee']['n'], 1)
    self.assertEqual(res.json['ddate'], date.today().strftime('%Y-%m-%d'))

  @pytest.mark.usefixtures('fix_many_features')
  def test_get(self):
    res = self.testapp.get('/v1/feature/', json.dumps({'name': ''}),
                           headers=self.headers, status=200)
    self.assertEqual(res.json.get('count_rows'), 15)
    # print(res.json)
    # print(res.json.get('results'))
    # self.assertEqual(res.json.get('name'), '-')
