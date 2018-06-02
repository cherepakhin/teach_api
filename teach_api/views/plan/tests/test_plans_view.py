import pytest
from pyramid import testing

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.plan.plans_view import PlansView


class PlansViewTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_create(self):
    params = {
        'employee_n': 1,
        'year': 2018,
        'month': 2,
        'qty_work': 10,
        'qty_question': 20,
    }
    request = testing.DummyRequest(json_body=params)
    context = testing.DummyResource()
    response = PlansView(context, request).post()
    self.assertEqual(response['n'], 2)
    self.assertEqual(response['year'], params['year'])
    self.assertEqual(response['month'], params['month'])
    self.assertEqual(response['qty_work'], params['qty_work'])
    self.assertEqual(response['qty_question'], params['qty_question'])
    self.assertEqual(response['employee']['n'], 1)
