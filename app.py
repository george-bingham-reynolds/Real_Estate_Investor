import os

from flask import Flask, request
from flask_smorest import Api

from db import db
import models #HAVE TO BE IMPORTED BEFORE SQLALCHEMY

from resources.city import blp as CityBlueprint
from resources.county import blp as CountyBlueprint

def create_app(db_url = None):

    app = Flask(__name__)



    app.config["PROPAGATE_EXCEPTIONS"] = True #BASICALLY SHOW EXCEPTIONS FROM LOWER PKGS
    app.config["API_TITLE"] = "Stores REST API" #TITLE OF OPERATIONS DOC
    app.config["API_VERSION"] = "v1" #VERSION OF API
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui" #USE SWAGGER FOR BUILDING DOCUMENTATION
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" #FOUND HERE
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URI", "sqlite:///data.db") #TRIES TO FUNC INPUT THEN GET ENV VAR THEN SQLITE STR 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app) #INIT F-SQL CONNECTION TO APP

    api = Api(app) #BASICALLY CONNECTS FLASK-SMOREST EXTENSION TO FLASK APP

    with app.app_context():
        db.create_all()


    api.register_blueprint(CityBlueprint)
    api.register_blueprint(CountyBlueprint)

    return app
