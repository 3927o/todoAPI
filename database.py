#encoding:utf-8
from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1/todoAPI'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = os.urandom(16)
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(500))
    finished = db.Column(db.Boolean, nullable=False)
    timeStart = db.Column(db.DateTime, nullable=False)
    timeEnd = db.Column(db.DateTime, nullable=False)

    def __init__(self, title, timeend, uid, *content):
        self.title = title
        self.finished = 0
        self.uid = uid
        self.timeStart = str(datetime.now())[0:19]
        self.timeEnd = timeend
        self.content = content


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self,username):
        self.username = username

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)  # python 3

    def getTasks(self, status=-1):
        if status == -1:
            tasks = Task.query.filter_by(uid=self.id).all()
        elif status == 0:
            tasks = Task.query.filter_by(uid=self.id, finished=0).all()
        else:
            tasks = Task.query.filter_by(uid=self.id, finished=1).all()
        return tasks


db.create_all()


# def get_tasks():
#     tasks = Task.query.all()
#     Tasks=[]
#     for task in tasks:
#         Tasks.append(make_public_task(task))
#     return Tasks


# def make_public_task(task):
#     Task={}
#     Task['uri']=url_for('task', id=task.id)
#     Task['title'] = task.title
#     Task['content'] = task.content
#     Task['finished'] = task.finished
#     Task['timestart'] = task.timeStart
#     Task['timeend'] = task.timeEnd
#     return Task


# print(get_tasks())