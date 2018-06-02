from crypt import crypt
import pytest

from teach_api.tests.base_test_db import BaseTestDB
from teach_api.views.login.security import groupfinder_in_db


class SecurityTest(BaseTestDB):

  @pytest.mark.usefixtures('fix_employees')
  def test_get_rules(self):
    rules = groupfinder_in_db('NAME_1', None)
    self.assertEqual(rules, ['question_edit'])

  # def test_crypt(self):
  #   cipher = crypt('password', 'secret service')
  #   print(cipher)
