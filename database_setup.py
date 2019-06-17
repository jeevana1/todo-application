from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todo'

    value = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    deleted = Column(String(10), nullable = False, default = "false")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'value': self.value,
            'deleted': self.deleted
        }

class SubTask(Base):
    __tablename__ = 'subtask'
    
    value = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    task_id = Column(Integer, ForeignKey('todo.id'))
    todo = relationship(Todo)


engine = create_engine('sqlite:///todo.db')

Base.metadata.create_all(engine)