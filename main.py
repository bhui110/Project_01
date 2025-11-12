from database import engine
from models import Base
from database import Session
from models import Product

import sys

def create():
    pass

def drop():
    pass


def main():
    try:
        if sys.arv[1] == "create":
            create()
        elif sys.arv[1] == "drop":
            drop()
        else:
            raise ValueError("not valid argument..")
        Base.metadata.create_all(engine)
        product = Product(name="eggs", price=12.34, available=100)
        session = Session()
        session.add(product)
        session.commit()
    except Exception as e:
        print(e)



if __name__ == "__main__":
    main()
