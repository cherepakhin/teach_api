import simplejson
from marshmallow import Schema, fields
# from teach_api.views.right.right_json import RightJSON


class EmployeeGroupJSON(Schema):

  n = fields.Integer()
  name = fields.Str()
  # rights = fields.Nested(RightJSON, many=True)

  class Meta:
    json_module = simplejson
