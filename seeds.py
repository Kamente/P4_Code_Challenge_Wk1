# Hey,don't mind this. i just used it to initially test the working of my database

from flask import Flask
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'

db.init_app(app)

app.app_context().push()

db.create_all()

restaurant1 = Restaurant(name="Dominion Pizza", address="Good Italian, Ngong Road, 5th Avenue")
restaurant2 = Restaurant(name="Pizza Hut", address="Westgate Mall, Mwanzi Road, Nrb 100")

db.session.add_all([restaurant1, restaurant2])

db.session.commit()

pizza1 = Pizza(name="Cheese", ingredients="Dough, Tomato Sauce, Cheese")
pizza2 = Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")

db.session.add_all([pizza1, pizza2])

db.session.commit()

restaurant_pizza1 = RestaurantPizza(
    price=13, pizza_id=pizza1.id, restaurant_id=restaurant1.id)
restaurant_pizza2 = RestaurantPizza(
    price=22, pizza_id=pizza2.id, restaurant_id=restaurant1.id)

db.session.add_all([restaurant_pizza1, restaurant_pizza2])

db.session.commit()

print("Data added successfully!")
