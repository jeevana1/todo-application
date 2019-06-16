from flask import Flask,render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Todo
import string


app = Flask(__name__)
# Connect to Database and create database session
engine = create_engine('sqlite:///todo.db')
Base.metadata.bind = engine

session = sessionmaker(bind=engine)

@app.route('/', methods=['GET', 'POST'])
def List():
    if request.method == 'GET':
        Items = session.query(Todo).all()
        return render_template('List.html', items = Items)