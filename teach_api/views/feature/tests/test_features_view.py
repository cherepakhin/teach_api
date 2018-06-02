import pytest
from pyramid import testing
from datetime import date

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.feature.features_view import FeaturesView


class FeaturesViewTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_features')
  def test_create(self):
    request = testing.DummyRequest(json_body={'n': 0,
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
                                              ],
                                              'employee_n': 1
                                              })
    context = testing.DummyResource()
    response = FeaturesView(context, request).post()
    self.assertEqual(response['n'], 2)
    self.assertEqual(response['name'], 'FEATURE_NAME')
    self.assertEqual(response['employee']['n'], 1)
    self.assertEqual(response['ddate'], date.today().strftime('%Y-%m-%d'))
