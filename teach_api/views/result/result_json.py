import simplejson
from marshmallow import Schema, fields
from teach_api.views.feature.feature_json import FeatureShortJSON
from teach_api.views.employee.employee_json import EmployeeShortJSON
from teach_api.views.question.question_json import QuestionWithFeatureJSON


class ResultJSON(Schema):

  n = fields.Integer()
  ddate = fields.DateTime(format='%Y-%m-%d')
  question_n = fields.Integer()
  answer_n = fields.Integer()
  employee_n = fields.Integer()
  is_correct = fields.Boolean()

  class Meta:
    json_module = simplejson
    dateformat = '%Y-%m-%d'


class ResultWithFeatureJSON(Schema):

  feature = fields.Nested(FeatureShortJSON)
  is_correct = fields.Boolean()

  class Meta:
    json_module = simplejson
    dateformat = '%Y-%m-%d'


class ResultEmployeeDetailJSON(Schema):

  n = fields.Integer()
  ddate = fields.DateTime(format='%Y-%m-%d')
  employee = fields.Nested(EmployeeShortJSON)
  is_correct = fields.Boolean()
  question = fields.Nested(QuestionWithFeatureJSON)
  is_correct = fields.Boolean()

  class Meta:
    json_module = simplejson
    dateformat = '%Y-%m-%d'


class ResultForPivotJSON(Schema):
  ddate = fields.DateTime(format='%Y-%m-%d')
  qty_all = fields.Integer()
  qty_ok = fields.Integer()


class PivotJSON(Schema):
  employee_name = fields.Str()
  qty_all = fields.Integer()
  qty_ok = fields.Integer()
  results = fields.Nested(ResultForPivotJSON, many=True)


class ResultForPivotCreateFeatureJSON(Schema):
  ddate = fields.DateTime(format='%Y-%m-%d')
  qty = fields.Integer()


class PivotCreateFeatureJSON(Schema):
  employee_name = fields.Str()
  qty = fields.Integer()
  results = fields.Nested(ResultForPivotCreateFeatureJSON, many=True)
