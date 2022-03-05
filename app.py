from flask import Flask
from flask_restful import Api
from resources.recipe import Recipes, Tags
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Recipes, "/recipes")
api.add_resource(Tags, "/recipes/tags")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
