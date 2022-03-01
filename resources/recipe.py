from argparse import Action
from email.policy import strict
import string
from typing import List
from tokenize import String
from flask_restful import Resource, reqparse
from sqlalchemy import false
from models.recipe import RecipeModel


class RecipesByTag(Resource):

    def get(self, tags: str):
        return {
            "recipes": [
                recipe.json()
                for recipe in RecipeModel.find_recipes_by_tags(tags)
            ]
        }, 200


class Tags(Resource):

    def get(self):
        return {"tags": RecipeModel.get_all_tags()}, 200


class Recipes(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "recipeId",
        type=str,
        required=True,
        help="This is the id of the recipe, can be left empty",
    )
    parser.add_argument(
        "name",
        type=str,
        required=True,
        help="This is the name of the recipe, can't be left empty",
    )
    parser.add_argument(
        "active_time",
        type=int,
        required=True,
        help="This is the active_time of the recipe, can't be left empty",
    )
    parser.add_argument(
        "total_time",
        type=int,
        required=True,
        help="This is the total_time of the recipe, can't be left empty",
    )
    parser.add_argument(
        "tags",
        type=str,
        action="append",
        required=False,
        help="This is the tags of the recipe, can be left empty",
    )
    parser.add_argument(
        "ingredients",
        type=str,
        action="append",
        required=True,
        help="This is the ingredients of the recipe, can't be left empty",
    )
    parser.add_argument(
        "instructions",
        type=str,
        action="append",
        required=True,
        help="This is the instructions of the recipe, can't be left empty",
    )

    def get(self):
        return {
            "recipes": [recipe for recipe in RecipeModel.find_all_recipes()]
        }

    def post(self):
        """
        The POST method is to create a new recipe. 
        If the exactly same recipe name already exits, it will return 400 error code.
        Otherwise, it will save the recipe to the database.
        """
        payload = Recipes.parser.parse_args()
        print(payload)
        recipe_name = payload["name"]
        if RecipeModel.find_recipe_by_recipe_name(recipe_name):
            return {
                "message":
                f"a recipe with name '{recipe_name}' already exists."
            }, 400
        recipe = RecipeModel(**payload)
        recipe.save_to_db()
        return recipe.json(), 201

    def put(self):
        """
        The PUT method is to update an existing recipe. The recipe_id must be included in the payload. 
        All other required arguments should also be included in the payload.
        """
        payload = Recipes.parser.parse_args()
        if "recipeId" not in payload:
            return {
                "message":
                "this payload must contain a recipe id in order to update it"
            }, 400
        recipe = RecipeModel.find_recipe_by_id(payload["recipeId"])
        if not recipe:
            return {"message": "the recipe id doesn't exist"}, 400
        else:
            recipe.name = payload.get("name", recipe.name)
            recipe.active_time = payload.get("active_time", recipe.active_time)
            recipe.total_time = payload.get("total_time", recipe.total_time)
            recipe.tags = payload.get("tags", recipe.tags)
            recipe.ingredients = payload.get("ingredients", recipe.ingredients)
            recipe.instructions = payload.get("instructions",
                                              recipe.instructions)
            recipe.save_to_db()
        return recipe.json(), 200
