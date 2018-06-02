import simplejson
from marshmallow import Schema, fields
from ..answer.answer_json import AnswerJSON


class FeatureShortJSON(Schema):

  n = fields.Integer()
  name = fields.Str()

  class Meta:
    json_module = simplejson


class QuestionJSON(Schema):

  n = fields.Integer()
  feature_n = fields.Integer()
  name = fields.Str()
  txt = fields.Str()
  answers = fields.Nested(AnswerJSON, many=True)

  class Meta:
    json_module = simplejson


class QuestionFullJSON(QuestionJSON):

  answer_n = fields.Integer()

  class Meta:
    json_module = simplejson


class QuestionWithFeatureJSON(QuestionFullJSON):
  feature = fields.Nested(FeatureShortJSON)

  class Meta:
    json_module = simplejson
