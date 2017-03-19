import time

from . import ModelMixin
from . import db


class Message(db.Model, ModelMixin):
    __tablename__ = 'msgs'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    username = db.Column(db.Text)
    created_time = db.Column(db.Integer, default=0)

    def __init__(self, form):
        self.content = form.get('content', '')
        self.username = form.get('username', '')
        self.created_time = int(time.time())
