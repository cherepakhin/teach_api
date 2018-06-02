import pytest
from datetime import date
# import json
# from pyramid_sqlalchemy import Session

# from teach_api.models import Report
from .atest_mdt import AViewTest


class ReportRestTest(AViewTest):

  @pytest.mark.usefixtures('fix_for_employee_feature_group')
  def test_employee_feature_group_get(self):
    self.testapp.get('/v1/report/employee_feature_group/',
                     {'year': 2018, 'month': 3},
                     headers=self.headers, status=200)
    # self.assertEqual(res.json.get('n'), 1)
    # print(res)
    # self.assertEqual(res.json.get('name'), '-')

  @pytest.mark.usefixtures('fix_for_employee_feature_group')
  def test_employee_detail(self):
    res = self.testapp.get('/v1/report/employee_detail/',
                           {'employee_name': 'NAME', 'year': date.today(
                           ).year, 'month': date.today().month},
                           headers=self.headers, status=200)
    for result in res.json:
      assert result['employee']['name'] == 'NAME'
    # self.assertEqual(res.json.get('n'), 1)
    # print(res)
    # self.assertEqual(res.json.get('name'), '-')

  @pytest.mark.usefixtures('fix_results_for_pivot_report')
  def test_pivot(self):
    res = self.testapp.get('/v1/report/pivot/',
                           {'year': date.today(
                           ).year, 'month': date.today().month},
                           headers=self.headers, status=200).json
    # print(res)
    assert len(res) == 1
    assert res[0]['employee_name'] == 'NAME'
    assert res[0]['qty_all'] == 5
    assert res[0]['qty_ok'] == 3
    results = res[0]['results']
    assert len(results) == 2

  @pytest.mark.usefixtures('fix_for_pivot_create_feature_report')
  def test_pivot_create_feature_report(self):
    res = self.testapp.get('/v1/report/pivot_create_feature/',
                           {'year': date.today(
                           ).year, 'month': date.today().month},
                           headers=self.headers, status=200).json
    # print(res)
    assert len(res) == 2
    assert res[0]['employee_name'] == 'EMPLOYEE_1'
    assert res[0]['qty'] == 2
    assert res[1]['employee_name'] == 'EMPLOYEE_2'
    assert res[1]['qty'] == 2

    results = res[0]['results']
    assert len(results) == 2

    results = res[1]['results']
    assert len(results) == 2
