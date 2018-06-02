import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from pyramid_sqlalchemy import Session, BaseObject, init_sqlalchemy

from ..models import Feature, Question, Answer, Employee, EmployeeGroup, Result, Right


def usage(argv):
  cmd = os.path.basename(argv[0])
  print('usage: %s <config_uri> [var=value]\n'
        '(example: "%s development.ini")' % (cmd, cmd))
  sys.exit(1)


def main(argv=sys.argv):
  if len(argv) < 2:
    usage(argv)
  config_uri = argv[1]
  options = parse_vars(argv[2:])
  setup_logging(config_uri)
  settings = get_appsettings(config_uri, options=options)
  engine = engine_from_config(settings, 'sqlalchemy.')
  init_sqlalchemy(engine)

  BaseObject.metadata.create_all()

  # with transaction.manager:
  #   Session.add(Topic(n=1, name='-'))
