from pyramid_sqlalchemy import Session

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.models import Employee


class EmployeeTest(BaseTestDB):

  def test_model_sets_n_automatically(self):
    employee = Employee(name='name_employee')
    Session.add(employee)
    Session.flush()
    assert employee.n is not None
    assert employee.name == 'name_employee'
