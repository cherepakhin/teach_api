import pytest
from pyramid import testing
from datetime import date
from dateutil.relativedelta import relativedelta

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.report.reports_view import ReportsView


class ReportsViewTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_for_employee_feature_group')
  def test_employee_feature_group(self):
    request = testing.DummyRequest(
        params={'year': date.today().year, 'month': date.today().month})
    context = testing.DummyResource()
    context.name_report = 'employee_feature_group'
    response = ReportsView(context, request).get()
    # print(response)
    self.assertEqual(response, [
        {
            "employee_name": "NAME_1",
            "feature_groups": [
                {"qty_all": 1, "qty_ok": 1, "name": None},
                {"qty_all": 1, "qty_ok": 0, "name": "GROUP_1"}],
            "qty_all": 2,
            "qty_ok": 1,
            "qty_plan": 1
        }, {
            "employee_name": "NAME_2",
            "feature_groups": [
                {"qty_all": 1, "qty_ok": 1, "name": "GROUP_1"},
                {"qty_all": 1, "qty_ok": 0, "name": "GROUP_2"}
            ],
            "qty_all": 2,
            "qty_ok": 1,
            "qty_plan": 2
        }
    ])

  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_for_employee_feature_group')
  def test_employee_detail(self):
    request = testing.DummyRequest(
        params={'employee_name': 'NAME_1', 'year': date.today().year, 'month': date.today().month})
    context = testing.DummyResource()
    context.name_report = 'employee_detail'
    response = ReportsView(context, request).get()
    # print(response)
    today = date.today().__str__()
    print(today)
    self.assertEqual(response,
                     [
                         {
                             "employee": {
                                 "name": "NAME_1",
                                 "n": 1
                             },
                             "ddate": today,
                             "is_correct": True,
                             "question": {
                                 "answer_n": 1,
                                 "feature_n": 1,
                                 "txt": "CONTENT_21",
                                 "answers": [],
                                 "feature": {
                                     "name": "-",
                                     "n": 1
                                 },
                                 "n": 21
                             },
                             "n": 1
                         },
                         {
                             "employee": {
                                 "name": "NAME_1",
                                 "n": 1
                             },
                             "ddate": today,
                             "is_correct": False,
                             "question": {
                                 "answer_n": 1,
                                 "feature_n": 2,
                                 "txt": "CONTENT_22",
                                 "answers": [],
                                 "feature": {
                                     "name": "FEATURE_1",
                                     "n": 2
                                 },
                                 "n": 22
                             },
                             "n": 2
                         }
                     ]
                     )

  @pytest.mark.usefixtures('fix_for_pivot_create_feature_report')
  def test_pivot_create_report(self):
    today = date.today()
    tomorrow = today + relativedelta(days=1)

    request = testing.DummyRequest(
        params={'year': today.year, 'month': today.month})
    context = testing.DummyResource()
    context.name_report = 'pivot_create_feature'
    response = ReportsView(context, request).get()
    # print(response)
    # print(today)
    self.assertEqual(response,
                     [
                         {
                             "employee_name": "EMPLOYEE_1",
                             "qty": 2,
                             "results": [
                                 {
                                     "ddate": today.__str__(),
                                     "qty": 1,
                                 },
                                 {
                                     "ddate": tomorrow.__str__(),
                                     "qty": 1,
                                 }
                             ]
                         },
                         {
                             "employee_name": "EMPLOYEE_2",
                             "qty": 2,
                             "results": [
                                 {
                                     "ddate": today.__str__(),
                                     "qty": 1,
                                 },
                                 {
                                     "ddate": tomorrow.__str__(),
                                     "qty": 1,
                                 }
                             ]
                         },

                     ])
