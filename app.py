from flask import Flask
from flask_restful import Api
# from resources.recipe import Recipes, Tags, RecipesByTag
from resources.recipe import Recipes, Tags
# from db import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)

api.add_resource(Recipes, "/recipes")
api.add_resource(Tags, "/recipes/tags")
# api.add_resource(RecipesByTag, "/recipes/<string:tags>")

# @app.before_first_request
# def create_tables():
#     db.create_all()

if __name__ == "__main__":
    # db.init_app(app)
    app.run(port=5000, debug=True)
