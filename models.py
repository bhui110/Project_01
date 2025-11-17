from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy import String, DECIMAL, Integer, ForeignKey, DateTime
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Product(Base):
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



# class Order(Base):
#     __tablename__ = "orders"
    
#     # Should have 2 foreign keys, refering to Customer and Product
#     products = mapped_column(ForeignKey("products.id"))
#     customer = mapped_column(ForeignKey("customers.id"))

#     price = mapped_column(float)
#     created = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

#     # Relations


class Customer(Base):
    __tablename__ = "customers"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    phone = mapped_column(String)

    # one to many
    # orders = relationship("Order", back_populates="Customers")

    def __repr__(self):
        return f"[Customer: id={self.id}, name={self.name}, phone={self.phone}]"
    
    def __str__(self):
        return f"The Customer {self.name} has phone number {self.phone}"
    
class Category(Base):
    __tablename__ = "categories"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"[Category: id={self.id}, Name={self.name}]"
