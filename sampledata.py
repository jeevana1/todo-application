from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Todo

engine = create_engine('sqlite:///todo.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

category1 = Todo(id=1,value="Hi this is first")

session.add(category1)
session.commit()
