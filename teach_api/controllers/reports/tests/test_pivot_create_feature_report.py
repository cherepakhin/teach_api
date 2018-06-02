from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import pytest
# from pyramid_sqlalchemy import Session
from teach_api.tests.base_test_db import BaseTestDB
from teach_api.controllers.reports.pivot_create_feature import PivotCreateFeatureReport
# from teach_api.models import Employee, Result

today = date.today()


class PivotCreateFeatureReportTest(BaseTestDB):

  def test_init(self):
    report = PivotCreateFeatureReport(today.year, today.month)
    assert report.year == today.year
    assert report.month == today.month
    assert report.start_date == date(today.year, today.month, 1)

  @pytest.mark.usefixtures('fix_for_pivot_create_feature_report')
  def test_get_records(self):
    today = date.today()

    records = PivotCreateFeatureReport(
        today.year, today.month).get_records()
    print(records)
    assert len(records) == 4

    assert records[0]['employee_name'] == 'EMPLOYEE_1'
    assert records[0]['ddate'] == today
    assert records[0]['qty'] == 1

    assert records[1]['employee_name'] == 'EMPLOYEE_1'
    assert records[1]['ddate'] == today + timedelta(days=1)
    assert records[1]['qty'] == 1

    assert records[2]['employee_name'] == 'EMPLOYEE_2'
    assert records[2]['ddate'] == today
    assert records[2]['qty'] == 1

    assert records[3]['employee_name'] == 'EMPLOYEE_2'
    assert records[3]['ddate'] == today + timedelta(days=1)
    assert records[3]['qty'] == 1

  def test_proccess(self):
    report = PivotCreateFeatureReport(today.year, today.month)
    data_report = report._process([],
                                  {'ddate': today, 'employee_name': 'NAME_1', 'qty': 2})
    # print(data_report)
    assert data_report[0]['employee_name'] == 'NAME_1'
    assert data_report[0]['qty'] == 2

    results = data_report[0]['results']
    assert results[0]['qty'] == 2

  @pytest.mark.usefixtures('fix_for_pivot_create_feature_report')
  def test_build(self):
    today = date.today()
    tomorrow = today + relativedelta(days=1)

    report = PivotCreateFeatureReport(today.year, today.month).build()
    # print(report)
    self.assertEqual(report,
                     [
                         {
                             "employee_name": "EMPLOYEE_1",
                             "qty": 2,
                             "results": [
                                 {
                                     "ddate": today,
                                     "qty": 1,
                                 },
                                 {
                                     "ddate": tomorrow,
                                     "qty": 1,
                                 }
                             ]
                         },
                         {
                             "employee_name": "EMPLOYEE_2",
                             "qty": 2,
                             "results": [
                                 {
                                     "ddate": today,
                                     "qty": 1,
                                 },
                                 {
                                     "ddate": tomorrow,
                                     "qty": 1,
                                 }
                             ]
                         },

                     ])
