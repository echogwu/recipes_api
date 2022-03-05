from typing_extensions import Required
from marshmallow import Schema, fields


class RecipeSearchSchema(Schema):
    name = fields.Str()
    active_time = fields.Int()
    total_time = fields.Int()
    tags = fields.Str()
    ingredients = fields.Str()


recipe_search_schema = RecipeSearchSchema()