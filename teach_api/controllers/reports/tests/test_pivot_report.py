from datetime import date
from dateutil.relativedelta import relativedelta
import pytest
# from pyramid_sqlalchemy import Session
from teach_api.tests.base_test_db import BaseTestDB
from teach_api.controllers.reports.pivot import PivotReport
# from teach_api.models import Employee, Result

today = date.today()


class PivotReportTest(BaseTestDB):

  def test_init(self):
    report = PivotReport(today.year, today.month)
    assert report.year == today.year
    assert report.month == today.month
    assert report.start_date == date(today.year, today.month, 1)

  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_results_for_pivot_report')
  def test_get_records(self):
    today = date.today()

    records_ok = PivotReport(today.year, today.month).get_records(True)
    print(records_ok)
    assert len(records_ok) == 2
    assert records_ok[0]['qty'] == 2
    assert records_ok[1]['qty'] == 1

    records_false = PivotReport(today.year, today.month).get_records(False)
    # print(records_false)
    assert len(records_false) == 2
    assert records_false[0]['qty'] == 1
    assert records_false[1]['qty'] == 1

  def test_proccess(self):
    report = PivotReport(today.year, today.month)
    report.for_ok = False
    data_report = report._process([],
                                  {'ddate': today, 'employee_name': 'NAME_1', 'qty': 2})
    # print(data_report)
    assert data_report[0]['employee_name'] == 'NAME_1'
    assert data_report[0]['qty_all'] == 2
    assert data_report[0]['qty_ok'] == 0

    results = data_report[0]['results']
    assert results[0]['qty_all'] == 2
    assert results[0]['qty_ok'] == 0

  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_results_for_pivot_report')
  def test_build(self):
    today = date.today()
    tomorrow = today + relativedelta(days=1)

    report = PivotReport(today.year, today.month).build()
    print(report)
    self.assertEqual(report,
                     [
                         {
                             "employee_name": "NAME_1",
                             "qty_all": 5,
                             "qty_ok": 3,
                             "results": [
                                 {
                                     "ddate": today,
                                     "qty_all": 3,
                                     "qty_ok": 2
                                 },
                                 {
                                     "ddate": tomorrow,
                                     "qty_all": 2,
                                     "qty_ok": 1
                                 }
                             ]
                         }
                     ])
