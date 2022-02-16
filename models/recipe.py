from re import I
import xxlimited
from db import db


class RecipeModel(db.Model):
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
        tags: str,
        ingredients: str,
        instructions: str,
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
        return cls.query.all()

    @classmethod
    def find_recipe_by_recipe_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_recipes_by_partial_recipe_name(cls, name: str):
        # return cls.query.filter_by(name=name)
        return cls.query.filter(cls.name.ilike(name)).all()

    @classmethod
    def find_recipes_by_ingredient_name(cls, ingredient: str):
        return cls.query.filter(cls.ingredients.ilike(ingredient)).all()

    @classmethod
    def find_recipe_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_recipes_by_tags(cls, tags: str):
        """
        example argument: "non_dairy,non_wheat,comfort_food"
        """
        tags = tags.split(",")
        result = set()
        for tag in tags:
            result = result.union(
                cls.query.filter(cls.tags.contains(tag)).all())
        return list(result)

    @classmethod
    def get_all_tags(cls):
        """
        return a list of unique tags.
        example result: ["comfort_food","non_dairy","non_wheat"]
        """
        entries = db.session.query(cls.tags).all()
        tags = set()
        for entry in entries:
            tags = tags.union(
                cls.parse_db_entry_string(attribute=cls.TAGS,
                                          string_to_be_parsed=entry[0]))
        return list(tags)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
