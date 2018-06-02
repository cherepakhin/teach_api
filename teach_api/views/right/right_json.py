from marshmallow import Schema


class RightJSON(Schema):

  class Meta:
    fields = (
        'n',
        'section',
        'access',
    )
