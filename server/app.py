#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.json.compact = False


db.init_app(app)  

migrate = Migrate(app, db)
api = Api(app)

class Index(Resource):

    def get(self):
        response_dict = {
            "index": "Welcome to the REST Create and Retrieve Lab",
        }

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response

api.add_resource(Index, '/')

class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        new_plant = Plant(
            name=request.form['name'],
            image=request.form['image'],
            price=request.form['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        response_dict = new_plant.to_dict()  

        response = make_response(jsonify(response_dict), 201)

        return response

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)

api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
