from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Initializing the Flask application

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'  # Database connection

db = SQLAlchemy(app)

# Define database models and their relationships
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)

    restaurant_pizzas = db.relationship(
        'RestaurantPizza', backref='restaurant', lazy='dynamic')

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)

    restaurant_pizzas = db.relationship(
        'RestaurantPizza', backref='pizza', lazy=True)

class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizza.id"), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        "restaurant.id"), nullable=False)

# Define the home route
@app.route('/')
def home():
    return {
        'message': 'Welcome to PizzaRestaurant'
    }, 200

# Route to get all restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurant_list = Restaurant.query.all()
    if restaurant_list:
        return jsonify([{'id': r.id, 'name': r.name, 'address': r.address} for r in restaurant_list]), 200  # Return 200 response to indicate success
    else:
        return jsonify({'error': "Restaurant not found"}), 404  # 404 response to indicate failure to get the restaurant

# Route to get a restaurant by ID
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'pizzas': [{'id': rp.pizza.id, 'name': rp.pizza.name, 'ingredients': rp.pizza.ingredients} for rp in restaurant.restaurant_pizzas]
        }
        return jsonify(restaurant_data), 200
    else:
        return jsonify({'error': "Restaurant not found"}), 404  # 404 response to indicate failure to get the restaurant

# Route to delete a restaurant by ID
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204  # Return 204 for a successful deletion
    else:
        return jsonify({'error': "Restaurant not found"}), 404

# Route to get all pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizza_list = Pizza.query.all()
    if pizza_list:
        return jsonify([{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in pizza_list]), 200
    else:
        return jsonify({'error': "Pizzas not found"}), 404

# Route to create a new restaurant-pizza relationship
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    if not price or not pizza_id or not restaurant_id:
        return jsonify({'errors': ["validation errors"]}), 400

    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not pizza or not restaurant:
        return jsonify({'errors': ["validation errors"]}), 400

    restaurant_pizza = RestaurantPizza(
        price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
    db.session.add(restaurant_pizza)
    db.session.commit()

    return jsonify({'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients}), 201

# Route to add a new restaurant
@app.route('/restaurants', methods=['POST'])
def add_new_restaurant():
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')

    if not name or not address:
        return jsonify({'errors': ["validation errors"]}), 400

    restaurant = Restaurant(name=name, address=address)
    db.session.add(restaurant)
    db.session.commit()

    return jsonify({'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address}), 201

# Route to add a new pizza
@app.route('/pizzas', methods=['POST'])
def add_new_pizza():
    data = request.get_json()
    name = data.get('name')
    ingredients = data.get('ingredients')

    if not name or not ingredients:
        return jsonify({'errors': ["validation errors"]}), 400

    pizza = Pizza(name=name, ingredients=ingredients)
    db.session.add(pizza)
    db.session.commit()

    return jsonify({'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients}), 201

if __name__ == '__main__':
    app.run(debug=True)
