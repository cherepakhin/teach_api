from pyramid.paster import get_app, setup_logging
ini_path = '/home/vasi/prog/py/teach_api/production.ini'
setup_logging(ini_path)
application = get_app(ini_path, 'main')