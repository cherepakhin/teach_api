import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.plan.plan_view import PlanView


class PlanViewTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_get(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 1
    response = PlanView(context, request).get()
    self.assertEqual(response['n'], 1)
    self.assertEqual(response['year'], 2017)
    self.assertEqual(response['month'], 12)
    self.assertEqual(response['employee']['n'], 1)

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_delete(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.n = 1
    response = PlanView(context, request).delete()
    self.assertEqual(response, {'status': 'success'})

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_update(self):
    request = testing.DummyRequest(json_body={'qty_work': 3})
    context = testing.DummyResource()
    context.n = 1
    response = PlanView(context, request).update()
    self.assertEqual(response.get('n'), 1)
    self.assertEqual(response.get('qty_work'), 3)
