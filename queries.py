from sqlalchemy import select
from db import Session
from models import Product, Customer, Category

def get_all_products():
    session = Session()
    stmt = select(Product)
    return session.execute(stmt).scalars().all()

def get_out_of_stock():
    session = Session()
    stmt = select(Product).where(Product.inventory < 1)
    return session.execute(stmt).scalars().all()

def find_products_in_category(cat_name):
    session = Session()
    stmt = (
        select(Product)
        .where(Product.category.has(Category.name == cat_name))
    )
    return session.execute(stmt).scalars().all()