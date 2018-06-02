import simplejson
from marshmallow import Schema, fields


class AnswerJSON(Schema):

  n = fields.Integer()
  txt = fields.Str()
  question_n = fields.Integer()

  class Meta:
    json_module = simplejson
