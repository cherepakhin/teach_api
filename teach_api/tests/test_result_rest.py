from datetime import date
from dateutil.relativedelta import relativedelta
import pytest
import json
from pyramid_sqlalchemy import Session

from teach_api.models import Result
from .atest_mdt import AViewTest


class ResultRestTest(AViewTest):

  @pytest.mark.usefixtures('fix_results_for_rest')
  def test_result_get(self):
    res = self.testapp.get('/v1/result/1/',
                           headers=self.headers, status=200)
    self.assertEqual(res.json.get('n'), 1)
    # print(res.json)
    self.assertEqual(res.json.get('question_n'), 21)
    self.assertEqual(res.json.get('answer_n'), 211)
    self.assertEqual(res.json.get('employee_n'), 1)
    self.assertEqual(res.json.get('is_correct'), True)

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_results_for_rest')
  def test_result_delete(self):
    res = self.testapp.delete(
        '/v1/result/1/', headers=self.headers, status=200)
    self.assertEqual(res.json, {'status': 'success'})
    results = Session.query(Result).all()
    assert len(results) == 1

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_results_for_rest')
  def test_result_post(self):
    res = self.testapp.post('/v1/result/1/',
                            json.dumps({'is_correct': False}), headers=self.headers, status=200)
    self.assertEqual(res.json.get('is_correct'), False)

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_results_for_rest')
  def test_results_post(self):
    res = self.testapp.post('/v1/result/',
                            json.dumps({'n': 3,
                                        'question_n': 31,
                                        'answer_n': 311,
                                        'is_correct': True,
                                        'employee_n': 1}),
                            headers=self.headers,
                            status=200)
    # self.assertEqual(res.json, {'n': 1})
    # print(res.json)
    self.assertEqual(res.json['n'], 3)
    self.assertEqual(res.json['question_n'], 31)
    self.assertEqual(res.json['answer_n'], 311)
    self.assertEqual(res.json['is_correct'], True)
    self.assertEqual(res.json['employee_n'], 1)

  def test_last_day(self):
    """
    Проверка вычисления последнего дня
    """
    year = 2017
    month = 12

    start_date = date(year, month, 1)
    end_date = start_date + relativedelta(months=1)
    assert end_date.year == 2018
    assert end_date.month == 1
    assert end_date.day == 1
