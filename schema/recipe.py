from typing_extensions import Required
from marshmallow import Schema, fields


class RecipeSchema(Schema):

    recipeId = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str()
    active_time = fields.Int()
    total_time = fields.Int()
    tags = fields.List(fields.Str())
    ingredients = fields.Dict(keys=fields.Str(),
                              values=fields.Dict(keys=fields.Str(),
                                                 values=fields.Str()))
    instructions = fields.List(fields.Str)


recipe_schema = RecipeSchema()