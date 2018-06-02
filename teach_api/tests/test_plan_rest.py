import pytest
import json
from pyramid_sqlalchemy import Session

from teach_api.models import Plan
from .atest_mdt import AViewTest


class PlanRestTest(AViewTest):

  @pytest.mark.usefixtures('fix_plan')
  def test_plan_get(self):
    res = self.testapp.get('/v1/plan/1/',
                           headers=self.headers, status=200)
    self.assertEqual(res.json.get('n'), 1)
    self.assertEqual(res.json.get('year'), 2017)
    self.assertEqual(res.json.get('month'), 12)
    self.assertEqual(res.json['employee']['n'], 1)

  @pytest.mark.usefixtures('fix_plan')
  def test_plan_delete(self):
    res = self.testapp.delete(
        '/v1/plan/1/', headers=self.headers, status=200)
    self.assertEqual(res.json, {'status': 'success'})
    plans = Session.query(Plan).all()
    assert len(plans) == 0

  @pytest.mark.usefixtures('fix_plan')
  def test_plan_post(self):
    res = self.testapp.post('/v1/plan/1/',
                            json.dumps({'qty_work': 3}), headers=self.headers, status=200)
    self.assertEqual(res.json.get('qty_work'), 3)

  @pytest.mark.usefixtures('fix_plan')
  def test_plans_post(self):
    params = {
        'employee_n': 1,
        'year': 2018,
        'month': 2,
        'qty_work': 10,
        'qty_question': 20,
    }
    res = self.testapp.post('/v1/plan/',
                            json.dumps(params), headers=self.headers, status=200)
    # self.assertEqual(res.json, {'n': 1})
    self.assertEqual(res.json.get('n'), 2)
    self.assertEqual(res.json.get('year'), 2018)

  @pytest.mark.usefixtures('fix_plan')
  def test_plan_get_on_month(self):
    res = self.testapp.get('/v1/plan/2017/12/',
                           headers=self.headers, status=200)
    self.assertEqual(len(res.json), 1)
    plan = res.json[0]
    self.assertEqual(plan['n'], 1)
    self.assertEqual(plan['year'], 2017)
    self.assertEqual(plan['month'], 12)
    self.assertEqual(plan['employee']['n'], 1)

  @pytest.mark.usefixtures('fix_plan')
  def test_plan_get_on_month_CREATE(self):
    res = self.testapp.get('/v1/plan/2018/10/',
                           headers=self.headers, status=200)
    self.assertEqual(len(res.json), 1)
    plan = res.json[0]
    self.assertEqual(plan['n'], 2)
    self.assertEqual(plan['year'], 2018)
    self.assertEqual(plan['month'], 10)
    self.assertEqual(plan['employee']['n'], 1)

  # @pytest.mark.usefixtures('fix_plan')
  # def test_plan_delete_month(self):
  #   res = self.testapp.delete(
  #       '/v1/plan/2017/12/', headers=self.headers, status=200)
  #   print(res)
  #   # self.assertEqual(res.json, {'status': 'success'})
  #   plans = Session.query(Plan).all()
  #   assert len(plans) == 0
