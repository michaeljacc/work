import hashlib
import os

from . import ModelMixin
from . import db
import time
import random


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    avatar = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)

    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()
        return m

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.avatar = form.get('avatar', 'http://vip.cocode.cc/uploads/avatar/default.png')
        self.created_time = int(time.time())

    def av(self):
        a = random.uniform(1, 2)
        a = int(a)
        path = '/static/images/avatar{}.jpg'.format(a)
        return path

    def valid(self):
        user = User.query.filter_by(username=self.username).first()
        if user is not None:
            return False
        return len(self.username) > 2 and len(self.password) > 2

    def validate_login(self, u):
        return u.username == self.username and u.password == self.password
