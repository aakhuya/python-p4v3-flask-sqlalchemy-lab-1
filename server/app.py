# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = db.session.get(Earthquake, id) 
    if earthquake:
        response = {
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }
        return make_response(jsonify(response), 200)
    else:
        response = {"message": f"Earthquake {id} not found."}
        return make_response(jsonify(response), 404)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()  # Query all earthquakes with magnitude >= parameter

    if earthquakes:
        response = {
            "count": len(earthquakes),
            "quakes": [ 
                {
                    "id": quake.id,
                    "location": quake.location,
                    "magnitude": quake.magnitude,
                    "year": quake.year
                }
                for quake in earthquakes
            ]
        }
        return make_response(jsonify(response), 200)
    else:
        response = {
            "count": 0,
            "quakes": [] 
        }
        return make_response(jsonify(response), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
