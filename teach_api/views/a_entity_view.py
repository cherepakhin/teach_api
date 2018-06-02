import logging
from teach_api.util.message_json import MessageJSON


class AEntityView(object):

  def __init__(self, context, request):
    self.context = context
    self.request = request
    self.log = logging.getLogger(__name__)

  def get(self):
    return self.serializator.dump(self.entity.get(self.context.n)).data

  def update(self, params={}):
    if params == {}:
      params = self.request.json_body
    if params == {}:
      raise Exception('Empty params for update')
    __entity = self.entity.update(self.context.n, params)
    return self.serializator.dump(__entity).data

  def delete(self):
    try:
      self.entity.delete(self.context.n)
    except Exception as e:
      error_message = 'Error delete n={}. Error: {}'.format(
          self.context.n, e)
      self.log.warning(error_message)
      return MessageJSON('Ошибка при удалении n=%s. Сообщение: %s' % (self.context.n, e))
    return {'status': 'success'}
