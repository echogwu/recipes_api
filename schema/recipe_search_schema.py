from typing_extensions import Required
from marshmallow import Schema, fields


class RecipeSearchSchema(Schema):
    name = fields.Str()
    active_time = fields.Int()
    total_time = fields.Int()
    tags = fields.List(fields.Str)
    ingredients = fields.List(fields.Str)


recipe_search_schema = RecipeSearchSchema()