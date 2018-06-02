import pytest

from datetime import date
from pyramid_sqlalchemy import Session
from teach_api.tests.base_test_db import BaseTestDB
from teach_api.controllers.feature_ctrl import FeatureCtrl
from teach_api.models import Feature, Question, Answer, FeatureGroup


class FeatureCtrlTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_many_features')
  def test_find(self):
    features = FeatureCtrl.find({'name': 'FEATURE'})
    self.assertEqual(len(features['results']), 10)
    self.assertEqual(features['count_rows'], 15)

  @pytest.mark.usefixtures('fix_many_features')
  def test_find_with_start_row(self):
    features = FeatureCtrl.find({'name': 'FEATURE', 'start_row': 10})
    self.assertEqual(len(features['results']), 5)
    self.assertEqual(features['count_rows'], 15)

  @pytest.mark.usefixtures('fix_many_features')
  def test_find_with_rows_per_page(self):
    features = FeatureCtrl.find({'name': 'FEATURE', 'rows_per_page': 2})
    self.assertEqual(len(features['results']), 2)
    self.assertEqual(features['count_rows'], 15)

  @pytest.mark.usefixtures('fix_features')
  def test_create(self):
    feature = {
        'n': 0,
        'name': 'FEATURE_NAME',
        'info': 'FEATURE_INFO',
        'info_profit': 'FEATURE_INFO_PROFIT',
        'employee_n': 1,
        'questions': [
                {
                    'n': 0,
                    'txt': 'QUESTION_TXT',
                    'answer_n': -3,
                    'answers': [
                        {'n': -1, 'txt': 'ANSWER_1'},
                        {'n': -2, 'txt': 'ANSWER_2'},
                        {'n': -3, 'txt': 'ANSWER_3'},
                        {'n': -4, 'txt': 'ANSWER_4'}
                    ],
                }
        ],
        'feature_group': [
            {
                'n': 1
            }
        ]
    }
    new_feature = FeatureCtrl.create(feature)
    self.assertEqual(new_feature.n, 2)
    self.assertEqual(new_feature.employee_n, 1)
    self.assertEqual(new_feature.ddate, date.today())
    question = Session.query(Question).filter(
        Question.feature_n == new_feature.n).one()
    self.assertEqual(question.txt, 'QUESTION_TXT')
    self.assertEqual(question.answer_n, 3)
    self.assertEqual(len(new_feature.feature_group), 1)
    self.assertEqual(new_feature.feature_group[0].n, 1)

  @pytest.mark.usefixtures('fix_full_fixteres')
  def test_update(self):
    feature = Feature.get(1)
    self.assertEqual(feature.n, 1)
    feature_param = {
        'n': 1,
        'name': 'FEATURE_NAME',
        'info': 'FEATURE_INFO',
        'info_profit': 'FEATURE_INFO_PROFIT',
        'employee_n': 1,
        'questions': [
                {
                    'n': 1,
                    'txt': 'QUESTION_TXT',
                    'answer_n': 3,
                    'answers': [
                        {'n': 1, 'txt': 'ANSWER_TXT_1'},
                        {'n': 2, 'txt': 'ANSWER_TXT_2'},
                        {'n': 3, 'txt': 'ANSWER_TXT_3'},
                    ],
                }
        ],
    }
    feature = FeatureCtrl.update(1, feature_param)
    self.assertEqual(feature.n, feature_param['n'])
    self.assertEqual(feature.name, feature_param['name'])
    self.assertEqual(feature.info, feature_param['info'])
    self.assertEqual(feature.info_profit, feature_param['info_profit'])
    self.assertEqual(feature.employee_n, 1)
    self.assertEqual(feature.ddate, date.today())
    self.assertEqual(feature.questions[0].txt, feature_param[
                     'questions'][0]['txt'])
    self.assertEqual(feature.questions[0].answer_n, feature_param[
                     'questions'][0]['answer_n'])
    self.assertEqual(feature.questions[0].n,
                     feature_param['questions'][0]['n'])
    for i in range(3):
      answer = feature.questions[0].answers[i]
      answer_param = feature_param['questions'][0]['answers'][i]
      self.assertEqual(answer.n, answer_param['n'])
      self.assertEqual(answer.txt, answer_param['txt'])

  @pytest.mark.usefixtures('fix_full_fixteres')
  def test_update_feature_group(self):
    feature = Feature.get(1)
    feature_group = FeatureGroup.get(1)
    feature.feature_group.append(feature_group)
    Session.flush()
    self.assertEqual(len(feature.feature_group), 2)
    feature_group_params = [
        {
            'n': 11
        }
    ]
    f_updated = FeatureCtrl.update_feature_group(feature, feature_group_params)
    self.assertEqual(len(f_updated.feature_group), 1)
    self.assertEqual(f_updated.feature_group[0].n, 11)
