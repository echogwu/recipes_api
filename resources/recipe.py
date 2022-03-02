from argparse import Action
from email.policy import strict
from flask import request
from typing import List
from tokenize import String
from flask_restful import Resource, reqparse
from sqlalchemy import false
from models.recipe import RecipeModel
from schema.recipe import recipe_schema
from schema.recipe_search_schema import recipe_search_schema
from request_utils import get_request_args


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

    def get(self):
        # needs to dump it with JsonDecimalEncoder because dynamodb returns decimal type instead of int
        # return {"recipes": RecipeModel.find_all_recipes()}
        print(get_request_args(recipe_search_schema))
        args = get_request_args(recipe_search_schema)
        return {"recipes": RecipeModel.find_recipes_by_args(args)}

    def post(self):
        """
        The POST method is to create a new recipe. 
        If the exactly same recipe name already exits, it will return 400 error code.
        Otherwise, it will save the recipe to the database.
        """
        payload = get_request_args(recipe_schema)
        recipe_name = payload["name"]
        if RecipeModel.find_recipe_by_recipe_name(recipe_name):
            return {
                "message":
                f"a recipe with name '{recipe_name}' already exists."
            }, 400
        recipe_id = payload["recipeId"]
        if RecipeModel.find_recipe_by_id(recipe_id):
            return {
                "message": f"a recipe with id '{recipe_id}' already exists."
            }, 400
        recipe = RecipeModel(**payload)
        recipe.save_to_db()
        return recipe.json(), 201

    def put(self):
        """
        The PUT method is to update an existing recipe. The recipe_id must be included in the payload. 
        All other required arguments should also be included in the payload.
        """
        payload = get_request_args(recipe_schema)
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
