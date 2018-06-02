from datetime import date
import pytest

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.controllers.report_ctrl import ReportCtrl


class ReportCtrlTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_employees')
  @pytest.mark.usefixtures('fix_for_employee_feature_group')
  def test_employee_detail(self):
    today = date.today()
    data = ReportCtrl.employee_detail('NAME_1', today.year, today.month)
    print(data)
    for result in data:
      assert result.employee_n == 1
