from random import randint, random
from datetime import datetime as dt
from datetime import timedelta
from app import app
from db import db
from models import Product, Category, Customer, Order, ProductOrder
from sqlalchemy import func, select
import csv
import sys

def create():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Tables Created!")

def drop():
    with app.app_context():
        db.drop_all()
        print("Tables Dropped...")

def import_products():
    with app.app_context():
        print("Importing products...")

        with open("data/products.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                name = row["name"]
                price = float(row["price"])
                inventory = int(row["available"])
                category = row["category"]

                # Check if category already exists
                possible_category = db.session.execute(
                    select(Category).where(Category.name == category)
                ).scalar()

                if not possible_category:
                    category_obj = Category(name=category)
                    db.session.add(category_obj)
                else:
                    category_obj = possible_category

                # Create Product
                prod = Product(
                    name=name,
                    price=price,
                    inventory=inventory,
                    category=category_obj
                )
                db.session.add(prod)

        db.session.commit()
        print("Products imported!")

def import_customers():
    with app.app_context():
        print("Importing customers...")

        with open("data/customers.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                cust = Customer(
                    name=row["name"],
                    phone=row["phone"]
                )
                db.session.add(cust)

        db.session.commit()
        print("Customers imported!")

def randomOrder():
    with app.app_context():
        for i in range(5):

            # Random customer
            customer = db.session.execute(
                select(Customer).order_by(func.random())
            ).scalar()

            # Create order with random created date
            created_time = (
                dt.now()
                - timedelta(
                    days=randint(1, 3),
                    hours=randint(0, 15),
                    minutes=randint(0, 30),
                )
            )

            order = Order(customer=customer, created=created_time)
            db.session.add(order)

            # Pick 4–6 random products
            num_prods = randint(4, 6)
            products = db.session.execute(
                select(Product).order_by(func.random()).limit(num_prods)
            ).scalars()

            # Create ProductOrder items
            for p in products:
                qty = randint(1, 5)
                po = ProductOrder(product=p, quantity=qty, order=order)
                db.session.add(po)

        db.session.commit()
        print("Random orders generated!")

    