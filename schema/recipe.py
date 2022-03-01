from typing_extensions import Required
from marshmallow import Schema, fields


class RecipeSchema(Schema):

    # class Meta:
    #     load_only = ("password", )
    #     dump_only = ("id", )

    id = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str()
    active_time = fields.Int()
    total_time = fields.Int()
    tags = fields.List()
    ingredients = fields.List()
    instructions = fields.List()