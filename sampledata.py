from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Todo, SubTask

engine = create_engine('sqlite:///todo.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

category1 = Todo(id=1,value="Hi this is first")

sub1 = SubTask(id = 1, value = "subtask 1", todo = category1, task_id = 1)
sub2 = SubTask(id = 2, value = "subtask 2", todo = category1, task_id = 1)

session.add(category1)
session.add(sub1)
session.add(sub2)
session.commit()
