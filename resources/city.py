import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import CityModel
from schemas import CitySchema

blp = Blueprint("Cities", __name__, description = "Operations on Cities")

@blp.route("/city/<string:place>")
class City(MethodView):

    @blp.response(200, CitySchema) #PASSES WHATEVER WE RETURN THRU SCHEMA
    def get(self, place):
        city = CityModel.query.get_or_404(place) # RETRIEVES CITY BY PRIMARY KEY
        return city
    
    def delete(self, place):
        city = CityModel.query.get_or_404(place)
        db.session.delete(city)
        db.session.commit()
        return{"message": "City deleted"}
    
    # NOTE - ADDING POST FUNCTIONALITY BELOW BUT NOT INCLUDING PUT FOR NOW (WANT TO ADD RECORDS BUT NOT MODIFY)

@blp.route("/city")
class CityList(MethodView):

    @blp.response(200, CitySchema(many = True))
    def get(self):
        return CityModel.query.all()
    
    @blp.arguments(CitySchema)
    @blp.response(201, CitySchema)
    def post(self, city_data):
        city = CityModel(**city_data)

        try:
            db.session.add(city)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "An error occurred while inserting the city")

        return city
    
    def delete(self):
        CityModel.query.delete()
        db.session.commit()
        return{"message": "deleted"}


    

# NOTE - POSTING CAPABILITY DOESN'T MAKE A TON OF SENSE FOR NOW; MAYBE IF I DO A LATER VERSION THAT CAN SERVE UP PREDS
