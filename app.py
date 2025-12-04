from pathlib import Path
from flask import Flask, redirect, render_template, request, url_for
from db import db
from models import Product, Category, Customer, Order, ProductOrder
from sqlalchemy import select

app = Flask(__name__)
# This will make Flask use a 'sqlite' database with the filename provided
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
# This will make Flask store the database file in the path provided
app.instance_path = Path("data").resolve()
# Adjust to your needs / liking. Most likely, you want to use "." for your instance path. This is up to you. You may also use "data".
db.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/products")
def products():
    stmt = db.select(Product).order_by(Product.name)
    products = db.session.execute(stmt).scalars().all()
    return render_template("products.html", products=products)

@app.route("/categories")
def categories():
    stmt = db.select(Category).order_by(Category.name)
    categories = db.session.execute(stmt).scalars().all()
    return render_template("categories.html", categories=categories)

@app.route("/categories/<string:name>")
def category_detail(name):
    stmt = db.select(Category).where(Category.name == name)
    category = db.session.execute(stmt).scalar()

    if not category:
        return f"Category '{name}' not found", 404

    return render_template("category_detail.html", category=category)

@app.route("/customers")
def customers():
    stmt = db.select(Customer).order_by(Customer.name)
    customers = db.session.execute(stmt).scalars().all()
    return render_template("customers.html", customers=customers)

@app.route("/customers/<int:id>")
def customer_detail(id):
    stmt = db.select(Customer).where(Customer.id == id)
    customer = db.session.execute(stmt).scalar()

    if not customer:
        return f"Customer with ID {id} not found", 404

    return render_template("customer_detail.html", customer=customer)

@app.route("/orders")
def orders():
    all_orders = db.session.execute(db.select(Order)).scalars()
    return render_template("orders.html", orders=all_orders)

@app.route("/orders/<int:id>")
def order(id):
    order_obj = db.session.get(Order, id)
    return render_template("order.html", order=order_obj)

@app.route("/orders/<int:id>/complete", methods=["POST"])
def complete_order(id):
    order_obj = db.session.get(Order, id)

    try:
        order_obj.complete()
        db.session.commit()
    except ValueError as e:
        return render_template("error.html", message=str(e)), 409

    return redirect(url_for("order", id=id))

if __name__ == "__main__":
    app.run(debug=True, port=8888)
