import pyramid.httpexceptions as exc
from pyramid.view import view_config
import logging
log = logging.getLogger(__name__)


@view_config(context=Exception, renderer='json')
def exception_view(context, request):
  # TODO: Выволить ошибки в файл
  log.error("The error was: %s" % context, exc_info=(context))
  return exc.HTTPBadRequest(json_body={'error': str(context)})
