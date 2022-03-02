from typing_extensions import Required
from marshmallow import Schema, fields


class RecipeSchema(Schema):

    # class Meta:
    #     load_only = ("password", )
    #     dump_only = ("id", )

    recipeId = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str()
    active_time = fields.Int()
    total_time = fields.Int()
    tags = fields.List(fields.Str)
    ingredients = fields.List(fields.Dict)
    instructions = fields.List(fields.Str)


recipe_schema = RecipeSchema()