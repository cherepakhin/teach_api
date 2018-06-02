class GetJSON(object):
  """docstring for GetJSON"""
  @classmethod
  def get_json(cls, entity):
    return cls().dump(entity).data
