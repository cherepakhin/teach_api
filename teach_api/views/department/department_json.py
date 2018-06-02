import simplejson
from marshmallow import Schema, fields


class DepartmentJSON(Schema):

  n = fields.Integer()
  name = fields.Str()

  class Meta:
    json_module = simplejson
