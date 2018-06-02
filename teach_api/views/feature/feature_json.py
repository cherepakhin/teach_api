import simplejson
from marshmallow import Schema, fields
from teach_api.views.question.question_json import QuestionFullJSON
from teach_api.views.feature_group.feature_group_json import FeatureGroupJSON
from teach_api.views.employee.employee_json import EmployeeShortJSON


class FeatureShortJSON(Schema):

  n = fields.Integer()
  name = fields.Str()
  info = fields.Str()
  info_profit = fields.Str()
  feature_group = fields.Nested(FeatureGroupJSON, many=True)
  employee = fields.Nested(EmployeeShortJSON)
  ddate = fields.DateTime(format='%Y-%m-%d')

  class Meta:
    json_module = simplejson


class FeatureFullJSON(FeatureShortJSON):

  questions = fields.Nested(QuestionFullJSON, many=True)

  class Meta:
    json_module = simplejson


class FeatureShortWithResultsJSON(Schema):

  count_rows = fields.Integer()
  results = fields.Nested(FeatureShortJSON, many=True)

  class Meta:
    json_module = simplejson


class FeatureFullWithResultsJSON(Schema):

  count_rows = fields.Integer()
  results = fields.Nested(FeatureFullJSON, many=True)

  class Meta:
    json_module = simplejson
