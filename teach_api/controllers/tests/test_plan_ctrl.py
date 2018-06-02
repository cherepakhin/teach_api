import pytest

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.controllers.plan_ctrl import PlanCtrl
from teach_api.models import Plan


class PlanCtrlTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_create(self):
    plan = PlanCtrl.create(1, 2000, 2, 10, 20)
    self.assertEqual(plan.n, 2)
    self.assertEqual(plan.employee_n, 1)
    self.assertEqual(plan.year, 2000)
    self.assertEqual(plan.month, 2)
    self.assertEqual(plan.qty_work, 10)
    self.assertEqual(plan.qty_question, 20)

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_create_for_params(self):
    params = {
        'employee_n': 1,
        'year': 2000,
        'month': 2,
        'qty_work': 10,
        'qty_question': 20
    }
    plan = PlanCtrl.create(**params)
    self.assertEqual(plan.n, 2)
    self.assertEqual(plan.employee_n, 1)
    self.assertEqual(plan.year, 2000)
    self.assertEqual(plan.month, 2)
    self.assertEqual(plan.qty_work, 10)
    self.assertEqual(plan.qty_question, 20)

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_create_for_arr_employees(self):
    nn_employees = [1, 2]
    plans = PlanCtrl.create_for_employees(nn_employees, 2000, 2, 10, 20)
    self.assertEqual(len(plans), 2)

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_create_on_month(self):
    plans = PlanCtrl.create_on_month(2000, 12)
    self.assertEqual(len(plans), 2)
    for plan in plans:
      self.assertEqual(plan.year, 2000)
      self.assertEqual(plan.month, 12)
      self.assertEqual(plan.qty_question, 0)
      self.assertEqual(plan.qty_work, 0)
    self.assertEqual(plans[0].employee.n, 1)
    self.assertEqual(plans[1].employee.n, 2)

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_find_by_date(self):
    params = {
        'year': 2017
    }
    plans = PlanCtrl.find(params)
    self.assertEqual(len(plans), 1)

    params = {
        'year': 2000
    }
    plans = PlanCtrl.find(params)
    self.assertEqual(len(plans), 0)

    params = {
        'month': 12
    }
    plans = PlanCtrl.find(params)
    self.assertEqual(len(plans), 1)

    params = {
        'year': 2000,
        'month': 12
    }
    plans = PlanCtrl.find(params)
    self.assertEqual(len(plans), 0)

    params = {
        'year': 2017,
        'month': 12
    }
    plans = PlanCtrl.find(params)
    self.assertEqual(len(plans), 1)

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_find_by_name(self):
    params = {
        'year': 2017,
        'employee_name': 'empl'
    }
    plans = PlanCtrl.find(params)
    self.assertEqual(len(plans), 1)

    params = {
        'year': 2017,
        'employee_name': '-empl'
    }
    plans = PlanCtrl.find(params)
    self.assertEqual(len(plans), 0)

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_update(self):
    plan = PlanCtrl.update_qty(1, {'qty_work': 3})
    self.assertEqual(plan.qty_work, 3)

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_delete_month(self):
    # Проверка , что лишнее не удаляется
    PlanCtrl.delete_month(3000, 12)
    plan = Plan.get(1)
    self.assertEqual(plan.n, 1)

    # А вот теперь должно удалиться
    PlanCtrl.delete_month(2017, 12)
    plans = PlanCtrl.find({})
    self.assertEqual(len(plans), 0)

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_get_on_month_create(self):
    # Планы создаются, если не созданы
    plans = PlanCtrl.get_on_month(3000, 12)
    self.assertEqual(len(plans), 2)

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_get_on_month_NOT_create(self):
    # Планы НЕ создаются
    plans = PlanCtrl.get_on_month(2017, 12)
    self.assertEqual(len(plans), 1)

  @pytest.mark.usefixtures('fix_employees_for_plan')
  @pytest.mark.usefixtures('fix_plan')
  def test_get_current_plan(self):
    plan = PlanCtrl.get_current_plan('EMPLOYEE1', 2017, 12)
    self.assertEqual(plan.year, 2017)
    self.assertEqual(plan.month, 12)
    self.assertEqual(plan.employee.name, 'EMPLOYEE1')
