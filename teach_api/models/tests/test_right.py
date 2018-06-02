import pytest
from pyramid_sqlalchemy import Session

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.models import Right, EmployeeGroup


class Right1Test(BaseTestDB):

  # @pytest.mark.skip
  @pytest.mark.usefixtures('fix_employees')
  def test_right_sets_n_automatically(self):
    # _group = Session.query(EmployeeGroup).filter(EmployeeGroup.n == 1).one()
    # assert _group.n == 1
    # _groups = Session.query(EmployeeGroup).all()
    # assert len(_groups) > 0
    right = Right(employee_group_n=1, section='doc', access='edit')
    Session.add(right)
    # Session.flush()
    # assert right.n is not None
    assert right.section == 'doc'
    assert right.access == 'edit'
    assert right.rule == 'doc_edit'

    rights = Right.find({'employee_n': 1})
    assert len(rights) == 2
    assert rights[0].section == 'doc'
    assert rights[0].access == 'edit'

    assert rights[1].section == 'question'
    assert rights[1].access == 'edit'
