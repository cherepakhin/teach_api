from datetime import date, timedelta, datetime
import pytest
from pydash import group_by, map_, sorted_uniq, find, order_by
from pyramid_sqlalchemy import Session

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.controllers.result_ctrl import ResultCtrl
from teach_api.models import Result, Employee


class ResultCtrlTest(BaseTestDB):

  # @pytest.mark.usefixtures('fix_employees')
  # @pytest.mark.usefixtures('fix_full_fixteres')
  # def test_exam_is_not_correct(self):
  #   result = ResultCtrl.exam(
  #       1, 1, 'NAME_1', '2018-06-01 22:23:24', '2018-06-01 22:23:25')
  #   self.assertEqual(result.question_n, 1)
  #   self.assertEqual(result.answer_n, 1)
  #   self.assertEqual(result.is_correct, False)
  #   self.assertEqual(result.employee.name, 'NAME_1')

  # Закомментировал, т.к. sqlite не переваривает даты
  # @pytest.mark.usefixtures('fix_employees')
  # @pytest.mark.usefixtures('fix_full_fixteres')
  # def test_exam_is_correct(self):
  #   result = ResultCtrl.exam(
  #       1, 2, 'NAME_1', '2018-06-01 22:23:24', '2018-06-01 22:23:25')
  #   self.assertEqual(result.question_n, 1)
  #   self.assertEqual(result.answer_n, 2)
  #   self.assertEqual(result.is_correct, True)
  #   self.assertEqual(result.employee.name, 'NAME_1')

  @pytest.mark.usefixtures('fix_report')
  def test_build_report(self):
    start_date = date.today().strftime('%Y-%m-%d')
    end_date = date.today().strftime('%Y-%m-%d')
    results = ResultCtrl.buildReport(start_date, end_date, '')
    self.assertEqual(len(results), 2)

  @pytest.mark.usefixtures('fix_report')
  def test_pydash(self):
    results = Session.query(Result).all()
    g = group_by(results, 'employee.name')
    # print(g)
    names = sorted_uniq(map_(results, 'employee.name'))
    # print(names)
    l = list(
        map(lambda name: {'employee_name': name, 'results': g[name]}, names))
    # print(l)
    start_date = date.today().strftime('%Y-%m-%d')
    end_date = (date.today() + timedelta(days=2)).strftime('%Y-%m-%d')
    ret = ResultCtrl.fill_empty_day_in_result(start_date, end_date, l)
    # print('---------------------')
    # print(ret[0]['results'])
    self.assertEqual(len(ret[0]['results']), 3)
    self.assertEqual(len(ret[1]['results']), 3)

  def test_generate_arr_days(self):
    arr_days = ResultCtrl.generate_arr_days('2017-12-01', '2017-12-05')
    self.assertEqual(len(arr_days), 5)
    self.assertEqual(arr_days[0], date(2017, 12, 1))
    self.assertEqual(arr_days[1], date(2017, 12, 2))
    self.assertEqual(arr_days[2], date(2017, 12, 3))
    self.assertEqual(arr_days[3], date(2017, 12, 4))
    self.assertEqual(arr_days[4], date(2017, 12, 5))

  def test_find_date(self):
    r1 = Result(n=1, ddate=date.today() + timedelta(days=1))
    r2 = Result(n=2, ddate=date.today())
    today = date.today()
    # self.assertEqual(r1.ddate, today)
    obj = {'employee_name': 'NAME', 'results': [r1, r2]}
    f = find(obj['results'], lambda x: x.ddate == today)
    self.assertIsNotNone(f)
    # print(arr_days)

  def test_sort_by_date(self):
    r1 = Result(n=1, ddate=date.today() + timedelta(days=1))
    r2 = Result(n=2, ddate=date.today())
    arr = [r1, r2]
    sorted_arr = order_by(arr, ['ddate'])
    self.assertEqual(sorted_arr[0], r2)
    # print(arr_days)

  @pytest.mark.usefixtures('fix_report')
  def test_already_answered(self):
    today = date.today()
    employee = Employee.get(1)
    qty_answered = ResultCtrl.count_answered(
        employee, today.year, today.month)
    assert qty_answered == 2

  @pytest.mark.usefixtures('fix_report')
  def test_find(self):
    today = date.today()
    params = {
        'employee_n': 1,
        'date': today
    }
    results = ResultCtrl.find(params)
    assert len(results) == 1
