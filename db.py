# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# engine = create_engine("sqlite:///store.db", echo=True)
# Session = sessionmaker(bind=engine)
