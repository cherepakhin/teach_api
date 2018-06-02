from pyramid_sqlalchemy import Session

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.models import EmployeeGroup


class EmployeeGroupTest(BaseTestDB):

  def test_model_sets_n_automatically(self):
    _group = EmployeeGroup(name='NAME_USERGROUP')
    Session.add(_group)
    Session.flush()
    assert _group.n is not None
    assert _group.name == 'NAME_USERGROUP'
