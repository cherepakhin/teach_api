import simplejson
from marshmallow import Schema, fields
from teach_api.views.employee_group.employee_group_json import EmployeeGroupJSON
from teach_api.views.department.department_json import DepartmentJSON


class EmployeeJSON(Schema):

  n = fields.Integer()
  name = fields.Str()
  employee_group = fields.Nested(EmployeeGroupJSON)
  department = fields.Nested(DepartmentJSON)

  class Meta:
    json_module = simplejson


class EmployeeShortJSON(Schema):

  n = fields.Integer()
  name = fields.Str()

  class Meta:
    json_module = simplejson
