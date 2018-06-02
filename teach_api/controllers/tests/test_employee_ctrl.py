import pytest

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.controllers.employee_ctrl import EmployeeCtrl


class EmployeeCtrlTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_employees')
  def test_find_by_name(self):
    employee = EmployeeCtrl.find_by_name('NAME_1')
    self.assertEqual(employee.n, 1)
    self.assertEqual(employee.name, 'NAME_1')
    self.assertEqual(employee.employee_group.name, 'admins')
    self.assertEqual(len(employee.employee_group.rights), 1)

  @pytest.mark.usefixtures('fix_employees')
  def test_find_by_like_name(self):
    employees = EmployeeCtrl.find_by_like_name('N')
    assert len(employees) > 0

  @pytest.mark.usefixtures('fix_disabled_employees')
  def test_find_disabled_employees(self):
    with pytest.raises(Exception) as e:
      EmployeeCtrl.find_by_name('NAME')
    assert 'Employee not found' in str(e.value)

  @pytest.mark.usefixtures('fix_employees')
  def test_find_by_name_exception(self):
    with pytest.raises(Exception) as e:
      EmployeeCtrl.find_by_name('NAME1')
    assert 'Employee not found' in str(e.value)

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_employees')
  def test_create(self):
    employee = EmployeeCtrl.create(
        name='NAME1', password='PASSWORD1', info='INFO1', employee_group_n=1, department_n=1)
    self.assertEqual(employee.n, 3)
    self.assertEqual(employee.name, 'NAME1')
    self.assertEqual(employee.password, 'PASSWORD1')
    self.assertEqual(employee.info, 'INFO1')

  @pytest.mark.usefixtures('fix_employees')
  def test_create_employee_group(self):
    employee_group = EmployeeCtrl.create_employee_group(name='NAME1')
    self.assertEqual(employee_group.n, 2)
    self.assertEqual(employee_group.name, 'NAME1')

  @pytest.mark.usefixtures('fix_employees')
  def test_add_right_to_employee_group(self):
    employee_group = EmployeeCtrl.add_right_to_employee_group(1, 'doc', 'edit')
    self.assertEqual(employee_group.n, 1)
    self.assertEqual(len(employee_group.rights), 2)

    self.assertEqual(employee_group.rights[0].section, 'doc')
    self.assertEqual(employee_group.rights[0].access, 'edit')

    self.assertEqual(employee_group.rights[1].section, 'question')
    self.assertEqual(employee_group.rights[1].access, 'edit')

  @pytest.mark.usefixtures('fix_employees')
  def test_delete_right(self):
    employee_group = EmployeeCtrl.delete_right(1)
    self.assertEqual(employee_group.n, 1)
    self.assertEqual(employee_group.name, 'admins')
    self.assertEqual(len(employee_group.rights), 0)

  @pytest.mark.usefixtures('fix_employees_for_plan')
  def test_find_all_worked(self):
    employees = EmployeeCtrl.find_all_worked()
    assert len(employees) == 2
