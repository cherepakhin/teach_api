import pytest
import json
from pyramid_sqlalchemy import Session

from teach_api.models import Department
from .atest_mdt import AViewTest


class DepartmentRestTest(AViewTest):

  @pytest.mark.usefixtures('fix_departments')
  def test_department_get(self):
    res = self.testapp.get('/v1/department/1/',
                           headers=self.headers, status=200)
    self.assertEqual(res.json.get('n'), 1)
    # print(res.json)
    self.assertEqual(res.json.get('name'), '-')

  # @pytest.mark.skip
  def test_department_delete(self):
    res = self.testapp.delete(
        '/v1/department/1/', headers=self.headers, status=200)
    self.assertEqual(res.json, {'status': 'success'})
    departments = Session.query(Department).all()
    assert len(departments) == 0

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_departments')
  def test_department_post(self):
    res = self.testapp.post('/v1/department/1/',
                            json.dumps({'name': 'NEW_NAME'}), headers=self.headers, status=200)
    self.assertEqual(res.json.get('name'), 'NEW_NAME')

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_departments')
  def test_departments_post(self):
    res = self.testapp.post('/v1/department/',
                            json.dumps({'name': 'NEW_NAME'}), headers=self.headers, status=200)
    # self.assertEqual(res.json, {'n': 1})
    self.assertEqual(res.json.get('n'), 2)
    self.assertEqual(res.json.get('name'), 'NEW_NAME')
