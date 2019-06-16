from flask import Flask,render_template,request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from database_setup import Base,Todo
import string


app = Flask(__name__)
# Connect to Database and create database session
engine = create_engine('sqlite:///todo.db')
Base.metadata.bind = engine

session = scoped_session(sessionmaker(bind=engine))

@app.teardown_request
def remove_session(ex=None):
    session.remove()

@app.route('/', methods=['GET', 'POST'])
def List():
    if request.method == 'POST':
        if request.form['value']:
            newItem = Todo(value = request.form['value'], deleted = "false")
            session.add(newItem)
            session.commit()
        Items = session.query(Todo).all()
        return render_template('List.html', items = Items)
    if request.method == 'GET':
        Items = session.query(Todo).all()
        return render_template('List.html', items = Items)