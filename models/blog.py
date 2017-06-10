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
