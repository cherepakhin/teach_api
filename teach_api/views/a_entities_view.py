

class AEntitiesView(object):

  def __init__(self, context, request):
    self.context = context
    self.request = request

  def get(self, params={}):
    if params == {}:
      params == self.request.params
    entities = self.entity.find(params)
    return self.serializator.dump(entities, many=True).data

  def create(self):
    params = self.request.json_body
    __entity = self.entity.create(params)
    return self.serializator.dump(__entity).data
