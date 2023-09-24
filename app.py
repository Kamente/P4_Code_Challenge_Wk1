from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'

db = SQLAlchemy(app)


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)

    pizzas = db.relationship('Pizza', backref='restaurants', lazy=True)


class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)

    restaurants = db.relationship('Restaurant', backref='pizzas', lazy=True)


class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey(
        "pizza.id"), nullable=False)  # foreign key for the pizza table
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        "restaurant.id"), nullable=False)  # foreign key for the restaurant table


@app.route('/')
def home():
    return {
        'message': 'Welcome to PizzaRestaurant'
    }, 200


@app.route('/restaurants', methods=['GET'])
def restaurants():
    restaurant_list = []
    for restaurant in Restaurant.query.all():
        restaurant_descr = {
            'name': restaurant.name,
            'address': restaurant.address
        }
        restaurant_list.append(restaurant_descr)

    if restaurant_list:
        return jsonify(restaurant_list), 200
    else:
        return jsonify({'error': "Restaurant not found"}), 404

# @app.route('restaurants/<int:id>', methods=['GET'])
# def restaurants(id):


@app.route('/pizzas', methods=['GET'])
def pizzas():
    pizza_list = []
    for pizza in Pizza.query.all():
        pizza_descr = {
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }
        pizza_list.append(pizza_descr)

    return jsonify(pizza_list), 200


if __name__ == '__main__':
    # db.create_all()
    app.run(port=5555, debug=True)
