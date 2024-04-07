import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import CountyModel
from schemas import CountySchema

blp = Blueprint("Counties", __name__, description = "Operations on Counties")

@blp.route("/county/<string:place>")
class County(MethodView):

    @blp.response(200, CountySchema) #PASSES WHATEVER WE RETURN THRU SCHEMA
    def get(self, place):
        county = CountyModel.query.get_or_404(place) # RETRIEVES COUNTY BY PRIMARY KEY
        return county
    
    def delete(self, place):
        county = CountySchema.query.get_or_404(place)
        db.session.delete(county)
        db.session.commit()
        return{"message": "County deleted"}
    

@blp.route("/county")
class CountyList(MethodView):

    @blp.response(200, CountySchema(many = True))
    def get(self):
        return CountyModel.query.all()
    

    @blp.arguments(CountySchema)
    @blp.response(201, CountySchema)
    def post(self, county_data):
        county = CountyModel(**county_data)

        try:
            db.session.add(county)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "An error occurred while inserting the county")

        return county
    
    def delete(self):
        CountyModel.query.delete()
        db.session.commit()
        return{"message": "deleted"}