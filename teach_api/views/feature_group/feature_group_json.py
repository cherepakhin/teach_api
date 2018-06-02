import simplejson
from marshmallow import Schema, fields


class FeatureGroupJSON(Schema):

  n = fields.Integer()
  name = fields.Str()
  parent_name = fields.Str()

  class Meta:
    json_module = simplejson


class FeatureGroupFullJSON(Schema):

  n = fields.Integer()
  name = fields.Str()
  parent_n = fields.Integer()
  parent_name = fields.Str()
  children = fields.Nested(FeatureGroupJSON, many=True)

  class Meta:
    json_module = simplejson
