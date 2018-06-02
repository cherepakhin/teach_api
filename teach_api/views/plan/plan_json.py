import simplejson
from marshmallow import Schema, fields
from teach_api.views.employee.employee_json import EmployeeJSON


class PlanJSON(Schema):

  n = fields.Integer()
  year = fields.Integer()
  month = fields.Integer()
  qty_work = fields.Integer()
  qty_question = fields.Integer()
  employee = fields.Nested(EmployeeJSON)

  class Meta:
    json_module = simplejson
