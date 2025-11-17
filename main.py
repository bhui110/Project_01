from db import engine, Session
from models import Base, Product, Category, Customer
from sqlalchemy import select
import sys
import csv

def create():
    Base.metadata.create_all(engine)
    print("Tables Created!")

def drop():
    Base.metadata.drop_all(engine)
    print("Tables Dropped...")

def import_products():
    session = Session()
    print("Importing products...")

    with open("data/products.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = row["name"]
            price = float(row["price"])
            inventory = int(row["available"])
            category = row["category"]

            # Check if category already exists
            possible_category = session.execute(
                select(Category).where(Category.name == category)
            ).scalar()

            if not possible_category:
                category_obj = Category(name=category)
                session.add(category_obj)
            else:
                category_obj = possible_category

            # Create Product
            prod = Product(
                name=name,
                price=price,
                inventory=inventory,
                category=category_obj
            )
            session.add(prod)

    session.commit()
    print("Products imported!")

def import_customers():
    session = Session()
    print("Importing customers...")

    with open("data/customers.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            cust = Customer(
                name=row["name"],
                phone=row["phone"]
            )
            session.add(cust)

    session.commit()
    print("Customers imported!")

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [create|drop|import_products|import_customers]")
        return

    command = sys.argv[1]

    if command == "create":
        create()
    elif command == "drop":
        drop()
    elif command == "import_products":
        import_products()
    elif command == "import_customers":
        import_customers()
    else:
        print("Invalid command.")

if __name__ == "__main__":
    main()
