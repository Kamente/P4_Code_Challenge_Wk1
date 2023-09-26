from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initializing the SQLAlchemy extension for Flask

# Defined the Restaurant model, which represents restaurants in the database
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(50), unique=True, nullable=False)  
    address = db.Column(db.String(100), nullable=False)  

    # Relationship between Restaurant and RestaurantPizza models.
    restaurant_pizzas = db.relationship(
        'RestaurantPizza', backref='restaurant', lazy=True)

# Defined the Pizza model, which represents pizza items in the database
class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(50), nullable=False)  
    ingredients = db.Column(db.String(255), nullable=False)  

    # Relationship between Pizza and RestaurantPizza models.
    restaurant_pizzas = db.relationship(
        'RestaurantPizza', backref='pizza', lazy=True)

# Defined the RestaurantPizza model, which represents the relationship between restaurants and pizzas
class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    price = db.Column(db.Integer, nullable=False)  
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizza.id"), nullable=False)  
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        "restaurant.id"), nullable=False) 
