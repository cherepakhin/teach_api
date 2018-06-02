# import pytest
import json
from pyramid_sqlalchemy import Session

from teach_api.models import Employee
from .atest_mdt import AViewTest


class EmployeeRestTest(AViewTest):

  # @pytest.mark.skip
  # @pytest.mark.usefixtures('fix_employees_for_test')
  def test_employee_get(self):
    # Session.flush()
    # print("\n******************test_employee_get")
    res = self.testapp.get('/v1/employee/1/',
                           headers=self.headers, status=200)
    self.assertEqual(res.json.get('n'), 1)
    # print(res.json)
    self.assertEqual(res.json.get('name'), 'NAME')
    self.assertEqual(res.json.get('employee_group').get('n'), 1)
    self.assertEqual(res.json.get('employee_group').get('name'), 'admins')
    # assert len(res.json.get('employee_group').get('rights')) > 0

  # @pytest.mark.skip
  def test_employee_delete(self):
    res = self.testapp.delete(
        '/v1/employee/1/', headers=self.headers, status=200)
    self.assertEqual(res.json, {'status': 'success'})
    employees = Session.query(Employee).all()
    assert len(employees) == 0

  # @pytest.mark.skip
  def test_employee_post(self):
    res = self.testapp.post('/v1/employee/1/',
                            json.dumps({'name': 'NEW_NAME'}), headers=self.headers, status=200)
    self.assertEqual(res.json.get('name'), 'NEW_NAME')

  # @pytest.mark.skip
  def test_employees_post(self):
    res = self.testapp.post('/v1/employee/',
                            json.dumps({'name': 'NEW_NAME'}), headers=self.headers, status=200)
    # self.assertEqual(res.json, {'n': 1})
    self.assertEqual(res.json.get('n'), 2)
    self.assertEqual(res.json.get('name'), 'NEW_NAME')
    self.assertEqual(res.json.get('employee_group').get('n'), 1)
    self.assertEqual(res.json.get('employee_group').get('name'), 'admins')
