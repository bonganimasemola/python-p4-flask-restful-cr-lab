from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_restful import Api, Resource, reqparse
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()

class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    price = db.Column(db.Float)

    def __init__(self, name, image, price):
        self.name = name
        self.image = image
        self.price = price

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name cannot be blank')
parser.add_argument('image', type=str, required=True, help='Image cannot be blank')
parser.add_argument('price', type=float, required=True, help='Price cannot be blank')

class Plants(Resource):
    def get(self):
        try:
            plants = Plant.query.all()
            return [plant.to_dict() for plant in plants], 
        except Exception as e:
            return {'error': str(e)}, 500

    def post(self):
        # args = parser.parse_args()
        # new_plant = Plant(name=args['name'], image=args['image'], price=args['price'])
        # OR
        # import pdb
        # pdb.set_trace()
        args = self.parser.parse_args()
        name = args.get('name')
        image = args.get('image')
        price = args.get('price')
        new_plant = Plant(name=name, image=image, price=price)
        

        try:
            db.session.add(new_plant)
            db.session.commit()
            return {"new_plant" :{
                'name': new_plant.name,
                'image': new_plant.image,
                'price': new_plant.price
            }}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
        finally:
            db.session.close()

class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get(plant_id)
        if plant:
            return plant.to_dict()
        else:
            return {'error': 'Plant not found'}, 404

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
