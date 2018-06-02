import pytest
from pyramid import testing
from pyramid_sqlalchemy import Session

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.plan.plans_month_view import PlansMonthView
from teach_api.models import Plan


class PlansMonthViewTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_get_month(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.year = 2017
    context.month = 12
    response = PlansMonthView(context, request).get()
    self.assertEqual(len(response), 1)
    plan = response[0]
    self.assertEqual(plan['year'], 2017)

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_delete(self):
    request = testing.DummyRequest()
    context = testing.DummyResource()
    context.year = 2017
    context.month = 12
    PlansMonthView(context, request).delete()
    plans = Session.query(Plan).filter(Plan.n == 1).all()
    self.assertEqual(len(plans), 0)
