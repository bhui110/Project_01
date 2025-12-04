from app import app
from db import db
from models import Product, Category, Customer
from sqlalchemy import select
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