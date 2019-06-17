from flask import Flask,render_template,request,redirect,url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from database_setup import Base,Todo,SubTask
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
        subItems = session.query(SubTask).all()
        return render_template('List.html', items = Items, sub = subItems)
    if request.method == 'GET':
        Items = session.query(Todo).all()
        subItems = session.query(SubTask).all()
        return render_template('List.html', items = Items, sub = subItems)

@app.route('/delete/<int:id>', methods = ['POST'])
def delete(id):
    item = session.query(Todo).filter_by(id=id).one()
    item.deleted = 'true'
    session.add(item)
    session.commit()
    Items = session.query(Todo).all()
    subItems = session.query(SubTask).all()
    return redirect(url_for('List', items=Items, sub = subItems))

@app.route('/recover/<int:id>', methods = ['POST'])
def recover(id):
    item = session.query(Todo).filter_by(id=id).one()
    item.deleted = 'false'
    session.add(item)
    session.commit()
    Items = session.query(Todo).all()
    subItems = session.query(SubTask).all()
    return redirect(url_for('List', items=Items, sub = subItems))

@app.route('/add/<int:id>/', methods = ['GET','POST'])
def addSubTask(id):
    if request.method == 'POST':
        Task = session.query(Todo).filter_by(id=id).one()
        if request.form['name']:
            newItem = SubTask(value = request.form['name'], todo = Task, task_id = id)
            session.add(newItem)
            session.commit()
        Items = session.query(Todo).all()
        subItems = session.query(SubTask).all()
        return redirect(url_for('List', items=Items, sub = subItems))
    if request.method == 'GET':
        return render_template('addSubTask.html')

@app.route('/deleteSubTask/<int:id>', methods = ['POST'])
def deleteSubTask(id):
    item = session.query(SubTask).filter_by(id=id).one()
    session.delete(item)
    session.commit()
    Items = session.query(Todo).all()
    subItems = session.query(SubTask).all()
    return redirect(url_for('List', items=Items, sub = subItems))


if __name__ == '__main__':
    connect_args={'check_same_thread':False},
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
