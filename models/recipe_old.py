from typing import List

from sqlalchemy import null
from db import dynamodb
from constants import RECIPE_TABLE_NAME
from boto3.dynamodb.conditions import Attr

table = dynamodb.Table(RECIPE_TABLE_NAME)


class RecipeModel():
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    active_time = db.Column(db.Integer)
    total_time = db.Column(db.Integer)
    # format for the tags attribute would be "non_dairy|non_wheat|comfort_food"
    tags = db.Column(db.String(500))
    # format for the ingredients would be "shreddd carrot/1 cup|coconut milk/6 ounces|ground chicken/1 lb"
    ingredients = db.Column(db.String)
    # format for the instructions would be "step 1 description|step 2 description|step_3 description"
    instructions = db.Column(db.String)

    TAGS = "tags"
    INGREDIENTS = "ingredients"
    INSTRUCTIONS = "instructions"

    def __init__(
        self,
        id: int,
        name: str,
        active_time: int,
        total_time: int,
        tags: List[str],
        ingredients: List[str],
        instructions: List[str],
    ):
        self.name = name
        self.active_time = active_time
        self.total_time = total_time
        self.tags = tags
        self.ingredients = ingredients
        self.instructions = instructions

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "active_time": self.active_time,
            "total_time": self.total_time,
            "tags": self.tags,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
        }

    @classmethod
    def parse_db_entry_string(cls, attribute: str, string_to_be_parsed: str):
        """
        This method is to convert strings stored in db as ingredients, instructions and tags into python list.
        # format for the `tags` attribute would be "non_dairy|non_wheat|comfort_food"
        # format for the `ingredients` would be "shreddd carrot/1 cup|coconut milk/6 ounces|ground chicken/1 lb"
        # format for the `instructions` would be "step 1 description|step 2 description|step_3 description"
        """
        allowed_attributes = [cls.TAGS, cls.INGREDIENTS, cls.INSTRUCTIONS]
        if attribute not in allowed_attributes:
            raise Exception(
                f"attribute name shoud be one of {allowed_attributes}")
        result = string_to_be_parsed.split("|")
        if attribute != cls.INGREDIENTS:
            return result
        else:
            all_ingredients = {}
            for ele in result:
                ingredient = ele.split("/")
                all_ingredients[ingredient[0]] = ingredient[1]
            return all_ingredients

    @classmethod
    def find_all_recipes(cls):
        return table.scan().get("Items")

    @classmethod
    def find_recipe_by_recipe_name(cls, name: str):
        response = table.scan(Limit=10,
                              Select='ALL_ATTRIBUTES',
                              ReturnConsumedCapacity='TOTAL',
                              FilterExpression=Attr('name').contains(name),
                              ConsistentRead=True)
        return response.get("Items")

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
    def find_recipe_by_id(cls, _id: int):
        result = table.get_item(Key={'id': _id}).get("Items")
        if not result:
            return None
        else:
            return result[0]

    @classmethod
    def find_recipes_by_tags(cls, tags: str):
        """
        find all the recipes that have all the tags
        """
        result = set()
        for tag in tags:
            # result = result.union(
            #     cls.query.filter(cls.tags.contains(tag)).all())
            recipes_with_a_specific_tag = set(
                table.scan(Limit=10,
                           Select='ALL_ATTRIBUTES',
                           ReturnConsumedCapacity='TOTAL',
                           FilterExpression=Attr('tags').contains(tag),
                           ConsistentRead=True).get("Items"))
            if result:
                result = result.intersection(recipes_with_a_specific_tag)
            else:
                result = recipes_with_a_specific_tag
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
        for ele in tags_list:
            tags.union(ele)
        return list(tags)

    def save_to_db(self):
        table.put_item(Item=self.json())

    def delete_from_db(self, _id: int):
        table.delete_item(Key={'id': _id})
