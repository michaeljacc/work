from . import ModelMixin
from . import db
from models.todo import Todo
import time
import random


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    avatar = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    weibo = db.relationship('Weibo', backref='user')
    comments = db.relationship('Comment', backref='user')
    todo = db.relationship('Todo', backref='user')

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.avatar = form.get('avatar', '/static/images/avatar (17)')
        self.created_time = int(time.time())

    def av(self):
        a = random.uniform(1, 2)
        a = int(a)
        path = './static/images/avatar{}.jpg'.format(a)
        return path

    def valid(self):
        user = User.query.filter_by(username=self.username).first()
        if user is not None:
            return False
        return len(self.username) > 2 and len(self.password) > 2

    def validate_login(self, u):
        return u.username == self.username and u.password == self.password

    def todos(self):
        td = Todo.query.filter_by(user_id=self.id).all()
        return td