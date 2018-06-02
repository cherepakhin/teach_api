import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.result.result_action_view import ResultActionView


class ResultsViewTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_full_fixteres')
  def test_exam_is_correct(self):
    request = testing.DummyRequest(
        json_body={
          'question_n': 1, 
          'answer_n': 2, 
          'employee_name': 'NAME_1', 
          'time_begin': '2018-06-01 22:23:24',
          'time_end': '2018-06-01 22:23:25'
        })
    context = testing.DummyResource()
    context.action = 'exam'
    response = ResultActionView(context, request).post()

    print(response)
    self.assertEqual(response['feature']['n'], 1)
    self.assertEqual(response['feature']['name'], 'FEATURE_1')
    self.assertEqual(response['feature']['info'], 'INFO_1')
    self.assertEqual(response['feature']['info_profit'], 'INFO_PROFIT_1')
    self.assertEqual(response['is_correct'], True)

  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_full_fixteres')
  def test_exam_is_not_correct(self):
    request = testing.DummyRequest(
        json_body={
          'question_n': 1, 
          'answer_n': 1, 
          'employee_name': 'NAME_1',
          'time_begin': '2018-06-01 22:23:24',
          'time_end': '2018-06-01 22:23:25'
        })
    context = testing.DummyResource()
    context.action = 'exam'
    response = ResultActionView(context, request).post()

    print(response)
    self.assertEqual(response['feature']['n'], 1)
    self.assertEqual(response['feature']['name'], 'FEATURE_1')
    self.assertEqual(response['feature']['info'], 'INFO_1')
    self.assertEqual(response['feature']['info_profit'], 'INFO_PROFIT_1')
    self.assertEqual(response['is_correct'], False)
