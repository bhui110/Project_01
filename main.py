from database import engine
from models import Base
from database import Session
from models import Product

def create():
    pass

def drop():
    pass


def main():
    Base.metadata.create_all(engine)
    product = Product(name="eggs", price=12.34, available=100)
    session = Session()
    session.add(product)
    session.commit()



if __name__ == "__main__":
    main()
