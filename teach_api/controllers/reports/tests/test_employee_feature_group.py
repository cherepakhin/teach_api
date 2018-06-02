from datetime import date
import pytest
import unittest
# import pprint
# from pydash import find
# import json
from teach_api.tests.base_test_db import BaseTestDB

from teach_api.controllers.reports.employee_feature_group import EmployeeFeatureGroupReport


class EmplyeeFeatureGroupTest(BaseTestDB):

  def test_build(self):
    rows = [
        {
            'employee_name': 'EMPLOYEE_1',
            'feature_group': 'FEATURE_GROUP_1',
            'qty': 1
        },
        {
            'employee_name': 'EMPLOYEE_1',
            'feature_group': 'FEATURE_GROUP_2',
            'qty': 1
        },
        {
            'employee_name': 'EMPLOYEE_1',
            'feature_group': 'FEATURE_GROUP_1',
            'qty': 1
        },
        {
            'employee_name': 'EMPLOYEE_2',
            'feature_group': 'FEATURE_GROUP_1',
            'qty': 1
        },
        {
            'employee_name': 'EMPLOYEE_2',
            'feature_group': 'FEATURE_GROUP_3',
            'qty': 1
        },
    ]
    _today = date.today()

    report_builder = EmployeeFeatureGroupReport(_today.year, _today.month)

    def mock_get_records(isOk):
      return rows

    report_builder.get_records = mock_get_records
    report = report_builder.build()

    # empl = find(report, {'employee_name': 'EMPLOYEE_1'})
    # assert empl['qty_all'] == 6
    # assert empl['qty_ok'] == 3
    # feature_groups = empl['feature_groups']
    # feature_group = find(feature_groups, {'name': 'FEATURE_GROUP_1'})
    # assert feature_group['qty_all'] == 4
    # assert feature_group['qty_ok'] == 2

    # empl = find(report, {'employee_name': 'EMPLOYEE_2'})
    # assert empl['qty_all'] == 4
    # assert empl['qty_ok'] == 2

    self.assertEqual(report, [
        {'employee_name': 'EMPLOYEE_1',
         'feature_groups': [
             {'name': 'FEATURE_GROUP_1',
              'qty_all': 4, 'qty_ok': 2},

             {'name': 'FEATURE_GROUP_2',
              'qty_all': 2, 'qty_ok': 1}
         ],
         'qty_all': 6,
         'qty_ok': 3,
         'qty_plan': 0},
        {'employee_name': 'EMPLOYEE_2',
         'feature_groups': [
             {'name': 'FEATURE_GROUP_1',
              'qty_all': 2, 'qty_ok': 1},
             {'name': 'FEATURE_GROUP_3',
              'qty_all': 2, 'qty_ok': 1}
         ],
         'qty_all': 4,
         'qty_ok': 2,
         'qty_plan': 0}
    ])
    # pp = pprint.PrettyPrinter(indent=2)
    # print('\n')
    # pp.pprint(report)

# SELECT employee.name AS employee_name, feature_group.name AS feature_group_name, count(*) AS count_1
# FROM result
# JOIN employee ON employee.n = result.employee_n
# JOIN question ON question.n = result.question_n
# JOIN feature ON feature.n = question.feature_n
# LEFT OUTER JOIN (feature_group_to_feature AS feature_group_to_feature_1
# JOIN feature_group ON feature_group.n = feature_group_to_feature_1.feature_group_n)
# ON feature.n = feature_group_to_feature_1.feature_n
# GROUP BY employee.name, feature_group.name
  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_for_employee_feature_group')
  def test_get_records(self):
    _today = date.today()
    report_builder = EmployeeFeatureGroupReport(_today.year, _today.month)

    # Проверка кол-ва ПРАВИЛЬНЫХ ответов
    records = report_builder.get_records(True)
    # print(records)
    self.assertEqual(records, [
        {'feature_group': None, 'qty': 1, 'employee_name': 'NAME_1'},
        {'feature_group': 'GROUP_1', 'qty': 1, 'employee_name': 'NAME_2'}
    ])

    # Проверка кол-ва ВСЕХ ответов
    records = report_builder.get_records(False)
    # print(records)
    # assert records[0][0] == 'NAME_1'
    self.assertEqual(records, [
        {'employee_name': 'NAME_1', 'feature_group': 'GROUP_1', 'qty': 1},
        {'employee_name': 'NAME_2', 'feature_group': 'GROUP_2', 'qty': 1}
    ])

  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_for_employee_feature_group')
  def test_build_on_DB(self):
    _today = date.today()
    report_builder = EmployeeFeatureGroupReport(_today.year, _today.month)
    report = report_builder.build()
    self.assertEqual(report, [
        {'employee_name': 'NAME_1',
         'feature_groups': [{'name': None, 'qty_all': 1, 'qty_ok': 1},
                            {'name': 'GROUP_1', 'qty_all': 1, 'qty_ok': 0}],
         'qty_all': 2,
         'qty_ok': 1,
         'qty_plan': 1,
         },
        {'employee_name': 'NAME_2',
         'feature_groups': [{'name': 'GROUP_1', 'qty_all': 1, 'qty_ok': 1},
                            {'name': 'GROUP_2', 'qty_all': 1, 'qty_ok': 0}],
         'qty_all': 2,
         'qty_ok': 1,
         'qty_plan': 2,
         }
    ])
    # pp = pprint.PrettyPrinter(indent=2)
    # print('\n')
    # pp.pprint(report)

  def test_convert_record_to_dict(self):
    result = [('NAME_1', None, 1),
              ('NAME_1', 'GROUP_1', 1),
              ('NAME_2', 'GROUP_1', 1),
              ('NAME_2', 'GROUP_2', 1)]
    # result = ('NAME_2', 'GROUP_2', 1)
    named_result = [
        dict(zip(['employee_name', 'feature_group', 'qty'], r)) for r in result]
    self.assertEqual(named_result, [{'employee_name': 'NAME_1', 'feature_group': None, 'qty': 1},
                                    {'employee_name': 'NAME_1',
                                     'feature_group': 'GROUP_1', 'qty': 1},
                                    {'employee_name': 'NAME_2',
                                     'feature_group': 'GROUP_1', 'qty': 1},
                                    {'employee_name': 'NAME_2', 'feature_group': 'GROUP_2', 'qty': 1}])
    # print(json.dumps(named_result))
    # pp = pprint.PrettyPrinter(indent=2)
    # print('\n')
    # pp.pprint(named_result)
