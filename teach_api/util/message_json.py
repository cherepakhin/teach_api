import simplejson as json
from pyramid.response import Response


class MessageJSON(Response):
  """docstring for MessageJSON"""

  def __init__(self, message):
    super().__init__(json.dumps({'message': message}))
    self.message = message
