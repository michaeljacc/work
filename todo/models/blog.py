import time

from . import ModelMixin
from . import db


class Blog(db.Model, ModelMixin):
    __tablename__ = 'blogs'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    author = db.Column(db.Text)
    created_time = db.Column(db.Integer, default=0)

    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.author = form.get('author', '')
        self.created_time = int(time.time())



class Comment(db.Model):
    __tablename__ = 'comments'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    author = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    #
    blog_id = db.Column(db.Integer)

    def __init__(self, form):
        self.content = form.get('content', '')
        self.author = form.get('author', '')
        self.blog_id = int(form.get('blog_id'))
        self.created_time = int(time.time())
