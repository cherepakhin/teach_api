import unittest
from pyramid import testing
from pyramid_sqlalchemy import Session, BaseObject
from pyramid.config import Configurator


class BaseTestDB(unittest.TestCase):

  def setUp(self):
    super(BaseTestDB, self).setUp()
    # self.config = Configurator()
    # Session.remove()
    self.config = testing.setUp(settings={
        'sqlalchemy.url': 'sqlite:///:memory:',
    })
    # self.config = testing.setUp(settings={
    #     'sqlalchemy.url': 'sqlite:///:memory:',
    # })
    # # self.config = testing.setUp(autoflush=False)
    self.config.include('pyramid_tm')
    self.config.include('pyramid_sqlalchemy')
    self.session = Session
    BaseObject.metadata.create_all()
    # print('create')
    # print(Session)

  def tearDown(self):
    testing.tearDown()
    Session.remove()
    super(BaseTestDB, self).tearDown()
