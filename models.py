from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy import String, DECIMAL, Integer, ForeignKey, DateTime
from datetime import datetime
from db import db

class Product(db.Model):
    __tablename__ = "product"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    price = mapped_column(DECIMAL(10, 2))
    inventory = mapped_column(Integer, default=0)

    category_id = mapped_column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")


    def __repr__(self):
        return f"[Product: {self.id}, Name: {self.name}, Price: {self.price}, Inventory: {self.inventory}]"

    def __str__(self):
        return f"The Product {self.name} costs {self.price} and {self.inventory} in stock!"



class Order(db.Model):
    __tablename__ = "orders"

    id = mapped_column(Integer, primary_key=True)

    customer_id = mapped_column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="orders")
    
    items = relationship('ProductOrder', back_populates='order')

    created = mapped_column(db.DateTime, nullable=False, default=db.func.now())
    completed = mapped_column(db.DateTime, nullable=True, default=None)
    amount = mapped_column(db.DECIMAL(6, 2), nullable=True, default=None)

    def estimate(self):
        total = 0
        for po in self.items:
            one = po.product.price * po.quantity
            total = total + one
        return total
    
    def complete(self):
        # Check inventory availability
        for po in self.items:
            if po.product.inventory < po.quantity:
                raise ValueError(
                    f"Not enough inventory for {po.product.name}! "
                    f"Requested {po.quantity}, available {po.product.inventory}"
                )

        # Subtract inventory
        for po in self.items:
            po.product.inventory -= po.quantity

        # Set completed time
        self.completed = db.func.now()

        # Compute amount
        self.amount = self.estimate()



class ProductOrder(db.Model):
    # Product foreign key
    product_id = mapped_column(db.ForeignKey("product.id"), primary_key=True)
    # Order foreign key
    order_id = mapped_column(db.ForeignKey("orders.id"), primary_key=True)
    # This is how many items we want in this order
    quantity = mapped_column(db.Integer, nullable=False)

    # Relationships and backreferences for SQL Alchemy
    product = relationship('Product')
    order = relationship('Order', back_populates='items')

class Customer(db.Model):
    __tablename__ = "customers"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    phone = mapped_column(String)

    # one to many
    orders = relationship("Order", back_populates="customer")

    def pending_orders(self):
        return [o for o in self.orders if o.completed is None]

    def completed_orders(self):
        return [o for o in self.orders if o.completed is not None]

    def __repr__(self):
        return f"[Customer: id={self.id}, name={self.name}, phone={self.phone}]"
    
    def __str__(self):
        return f"The Customer {self.name} has phone number {self.phone}"
    
class Category(db.Model):
    __tablename__ = "categories"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"[Category: id={self.id}, Name={self.name}]"
