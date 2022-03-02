from typing import List

from db import dynamodb
from constants import RECIPE_TABLE_NAME
from boto3.dynamodb.conditions import Attr, Key
from json_encoder import JsonDecimalEncoder
import json

table = dynamodb.Table(RECIPE_TABLE_NAME)


class RecipeModel():

    def __init__(
        self,
        recipeId: str,
        name: str,
        description: str = None,
        active_time: int = None,
        total_time: int = None,
        tags: List[str] = None,
        ingredients: List[dict] = None,
        instructions: List[str] = None,
    ):
        self.recipeId = recipeId
        self.name = name
        self.description = description
        self.active_time = active_time
        self.total_time = total_time
        self.tags = tags
        self.ingredients = ingredients
        self.instructions = instructions

    def json(self):
        return {
            "recipeId": self.recipeId,
            "name": self.name,
            "description": self.description,
            "active_time": self.active_time,
            "total_time": self.total_time,
            "tags": self.tags,
            "ingredients": self.ingredients,
            "instructions": self.instructions
        }

    @classmethod
    def jsonify(cls, recipe: dict) -> json:
        # input recipe is the original recipe dict we get from dynamodb that has decimal type instead of int
        return json.loads(json.dumps(recipe, cls=JsonDecimalEncoder))

    @classmethod
    def _find_all_recipes(cls) -> List["RecipeModel"]:
        return [(RecipeModel.jsonify(recipe))
                for recipe in table.scan().get("Items")]

    @classmethod
    def find_recipes_by_args(cls, args: dict) -> List["RecipeModel"]:
        if not args:
            return RecipeModel._find_all_recipes()
        name = args.get("name")
        tags = args.get("tags")  # TODO parse it so filter expression can work
        active_time = int(args.get("active_time", 0))
        total_time = int(args.get("total_time", 0))
        ingredients = args.get(
            "ingredients")  # TODO parse it so filter expression can work

        print(f"active_time: {active_time}")

        filter_expression = ''
        if name:
            filter_expression = Attr('name').contains(name)
        if tags:
            filter_expression = filter_expression & Attr('tags').contains(
                tags) if filter_expression else Attr('tags').contains(tags)
        if active_time:
            filter_expression = filter_expression & Attr('active_time').lte(
                active_time) if filter_expression else Attr('active_time').lte(
                    active_time)
        if total_time:
            filter_expression = filter_expression & Attr('total_time').lte(
                total_time) if filter_expression else Attr('total_time').lte(
                    total_time)
        if ingredients:
            filter_expression = filter_expression & Attr(
                "ingredients").contains(
                    ingredients) if filter_expression else Attr(
                        "ingredients").contains(ingredients)
        print(f"active_time: {active_time}")
        print(f"filter_expression: {filter_expression}")
        recipes = table.scan(Select='ALL_ATTRIBUTES',
                             Limit=10,
                             FilterExpression=filter_expression).get("Items")
        return [(RecipeModel.jsonify(recipe)) for recipe in recipes]

    @classmethod
    def find_recipes_by_partial_name(cls, partial_name: str):
        response = table.query(
            IndexName='nameIndex',
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression=Key('name').eq(partial_name))
        return [
            RecipeModel.jsonify(recipe) for recipe in response.get("Items")
        ]

    @classmethod
    def find_recipe_by_recipe_name(cls, name: str):
        result = table.query(
            IndexName='nameIndex',
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression=Key('name').eq(name)).get("Items")
        return RecipeModel(
            **RecipeModel.jsonify(result[0])) if result else None

    @classmethod
    def find_recipes_by_ingredient_name(cls, ingredient: str):
        response = table.scan(
            Limit=10,
            Select='ALL_ATTRIBUTES',
            ReturnConsumedCapacity='TOTAL',
            FilterExpression=Attr('ingredients.name').contains(ingredient),
            ConsistentRead=True)
        return [
            RecipeModel.jsonify(recipe) for recipe in response.get("Items")
        ]

    @classmethod
    def find_recipe_by_id(cls, recipeId: int) -> "RecipeModel":
        recipe = table.get_item(Key={'recipeId': recipeId}).get("Item")
        return RecipeModel(**RecipeModel.jsonify(recipe)) if recipe else None

    @classmethod
    def find_recipes_by_tags(cls, tags: str):
        """
        find all the recipes that have all the tags
        """
        recipes = set()
        for tag in tags:
            recipes_with_a_specific_tag = set(
                table.scan(Limit=10,
                           Select='ALL_ATTRIBUTES',
                           ReturnConsumedCapacity='TOTAL',
                           FilterExpression=Attr('tags').contains(tag),
                           ConsistentRead=True).get("Items"))
            if recipes:
                recipes = recipes.intersection(recipes_with_a_specific_tag)
            else:
                recipes = set(recipes_with_a_specific_tag)
        recipes = list(recipes)
        return [RecipeModel.jsonify(recipe) for recipe in recipes]

    @classmethod
    def get_all_tags(cls):
        """
        return a list of unique tags.
        example result: ["comfort_food","non_dairy","non_wheat"]
        """
        tags = set()
        response = table.scan(Limit=100,
                              Select='SPECIFIC_ATTRIBUTES',
                              AttributesToGet=['tags'],
                              ReturnConsumedCapacity='TOTAL',
                              ConsistentRead=True)
        tags_list = response.get("Items")
        for ele in tags_list:
            tags = tags.union(ele.get("tags"))
        return list(tags)

    def save_to_db(self):
        table.put_item(Item=self.json())

    def delete_from_db(self, recipe_id: int):
        table.delete_item(Key={'recipeId': recipe_id})
