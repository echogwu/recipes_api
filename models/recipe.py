from typing import List

from db import dynamodb
from constants import RECIPE_TABLE_NAME
from boto3.dynamodb.conditions import Attr

table = dynamodb.Table(RECIPE_TABLE_NAME)


class RecipeModel():

    def __init__(
        self,
        recipeId: str,
        name: str,
        active_time: int,
        total_time: int,
        tags: List[str],
        ingredients: List[str],
        instructions: List[str],
    ):
        self.recipeId = recipeId
        self.name = name
        self.active_time = active_time
        self.total_time = total_time
        self.tags = tags
        self.ingredients = ingredients
        self.instructions = instructions

    def json(self):
        return {
            "recipeId": self.recipeId,
            "name": self.name,
            "active_time": self.active_time,
            "total_time": self.total_time,
            "tags": self.tags,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
        }

    @classmethod
    def find_all_recipes(cls):
        return table.scan().get("Items")

    @classmethod
    def find_recipes_by_partial_name(cls, partial_name: str):
        response = table.scan(
            Limit=10,
            Select='ALL_ATTRIBUTES',
            ReturnConsumedCapacity='TOTAL',
            FilterExpression=Attr('name').contains(partial_name),
            ConsistentRead=True)
        return response.get("Items")

    @classmethod
    def find_recipe_by_recipe_name(cls, name: str):
        print(f"count: {table.item_count}")
        if not table.item_count:  # dynamodb updates every 6 hours or so,  recent changes might not be reflected in this value.
            return None
        result = table.get_item(Key={'name': name}).get("Items")
        print(f"result: {result}")
        return result[0] if result else None

    @classmethod
    def find_recipes_by_ingredient_name(cls, ingredient: str):
        response = table.scan(
            Limit=10,
            Select='ALL_ATTRIBUTES',
            ReturnConsumedCapacity='TOTAL',
            FilterExpression=Attr('ingredients.name').contains(ingredient),
            ConsistentRead=True)
        return response.get("Items")

    @classmethod
    def find_recipe_by_id(cls, recipeId: int):
        result = table.get_item(Key={'recipeId': recipeId}).get("Items")
        return result[0] if result else None

    @classmethod
    def find_recipes_by_tags(cls, tags: str):
        """
        find all the recipes that have all the tags
        """
        result = set()
        for tag in tags:
            recipes_with_a_specific_tag = set(
                table.scan(Limit=10,
                           Select='ALL_ATTRIBUTES',
                           ReturnConsumedCapacity='TOTAL',
                           FilterExpression=Attr('tags').contains(tag),
                           ConsistentRead=True).get("Items"))
            if result:
                result = result.intersection(recipes_with_a_specific_tag)
            else:
                result = set(recipes_with_a_specific_tag)
        return list(result)

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
        # TODO what's the output of tags_list??
        for ele in tags_list:
            tags = tags.union(ele)
        return list(tags)

    def save_to_db(self):
        table.put_item(Item=self.json())

    def delete_from_db(self, recipeId: int):
        table.delete_item(Key={'recipeId': recipeId})
