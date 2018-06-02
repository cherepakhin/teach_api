import pytest
import unittest
import webtest
import webtest.debugapp
from pyramid import testing
# from pyramid_sqlalchemy.testing import DatabaseTestCase
from pyramid_sqlalchemy import Session

from teach_api import main


@pytest.mark.usefixtures('fix_employees_for_test')
class AViewTest(unittest.TestCase):
  """
  Базовый класс для проведения тестов view
  """

  def setUp(self):
    super(AViewTest, self).setUp()
    settings = {'jwtauth.master_secret': 'secret service',
                'jwtauth.find_groups': 'teach_api.views.login.security:groupfinder_in_db'}

    # self.config = testing.setUp()
    # self.config.include('teach_api')

    app = main({}, **settings)
    self.testapp = webtest.TestApp(app)
    # Для редакторов
    token = "\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJOQU1FIiwibmFtZSI6Ik5BTUUifQ.STbVpwnDiWoyYWxao8a-yR-ji_F4ceea8-UfHSgkiVM\""
    # Для читателей
    # token = "\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ2aWV3ZXIifQ.Ja44sqvOtcYPMmqQ_vfsGGZOuVdstbYtV0aK_-DW0XM\""
    # Для тестов с авторизацией в запрос вставить headers
    # Пример: res =
    # self.testapp.get('/pyshop/v1/price/1/',headers=self.headers, status=200)
    self.headers = dict(Authorization='JWT token=' + token,)

  def tearDown(self):
    testing.tearDown()
    # Session.remove()
    super(AViewTest, self).tearDown()
