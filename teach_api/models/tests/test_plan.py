import pytest
from pyramid_sqlalchemy import Session

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.models import Plan


class PlanTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_plan')
  def test_model_sets_n_automatically(self):
    plan = Plan(employee_n=1, year=2000, month=1)
    Session.add(plan)
    Session.flush()
    assert plan.n is not None
    assert plan.employee_n == 1
    assert plan.year == 2000
    assert plan.month == 1
