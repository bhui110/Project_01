from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, DECIMAL, Integer
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "product"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    price = mapped_column(DECIMAL(10, 2))
    inventory = mapped_column(Integer, default=0)
    category = mapped_column(String)


class Order(Base):
    __tablename__ = "Order"

    products = mapped_column()

class Customer(Base):
    __tablename__ = "Customer"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    phone = mapped_column(String)
    orders = relationship("Order")

# class Category(Base):
#     __tablename__ = "categories"

#     id = mapped_column(Integer, primary_key=True)
#     name = mapped_column(String)
#     products = relationship("Product", back_populates="category")
