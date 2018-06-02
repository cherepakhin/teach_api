import pytest
from pyramid_sqlalchemy import Session

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.models import Department


class DepartmentTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_departments')
  def test_model_sets_n_automatically(self):
    department = Department(name='name_department')
    Session.add(department)
    Session.flush()
    assert department.n is not None
    assert department.name == 'name_department'

  @pytest.mark.usefixtures('fix_departments')
  def test_get_default(self):
    department = Department.get_default()
    assert department.n == 1
    assert department.name == '-'
