import time

from . import ModelMixin
from . import db
from models.user import User


class Weibo(db.Model, ModelMixin):
    __tablename__ = 'weibos'
    id = db.Column(db.Integer, primary_key=True)
    weibo = db.Column(db.String())
    name = db.Column(db.String())
    created_time = db.Column(db.String(), default=0)
    avart = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='weibo')
    avatar = db.Column(db.String(), default=0)

    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.weibo = form.get('weibo', '')
        self.name = form.get('name', '')
        self.created_time = dt
        self.comment = ''
        self.comments_num = 0

    def valid(self):
        return len(self.weibo) > 0 and len(self.name) > 0

    def comments(self):
        cs = Comment.query.filter_by(weibo_id=self.id).all()
        return cs

    def get_avatar(self):
        a = User.query.filter_by(username=self.name).first()
        if a is None:
            return 'http://k1.jsqq.net/uploads/allimg/1612/140F5A32-6.jpg'
        return 'http://k1.jsqq.net/uploads/allimg/1612/140F5A32-6.jpg'
    def error_message(self):
        if len(self.weibo) <= 2:
            return '微博太短了，至少要 3 个字符'
        elif len(self.weibo) >= 10:
            return '微博不能大于9个字符'

    def json(self):
        d = dict(
            id=self.id,
            weibo=self.weibo,
            name=self.name,
            created_time=self.created_time,
            avatar=self.get_avatar(),
            comments_num=len(self.comments()),
        )
        return d


class Comment(db.Model, ModelMixin):
    __tablename__ = 'comments'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String())
    name = db.Column(db.String())
    created_time = db.Column(db.String(), default=0)
    weibo_id = db.Column(db.Integer, db.ForeignKey('weibos.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    avatar = db.Column(db.String(), default=0)

    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.comment = form.get('comment', '')
        self.name = form.get('name', '')
        self.weibo_id = form.get('weibo_id', '')
        self.created_time = dt

    def valid(self):
        return len(self.comment) > 0 and len(self.name) > 0

    def get_avatar(self):
        a = User.query.filter_by(username=self.name).first()
        if a is None:
            return 'http://k1.jsqq.net/uploads/allimg/1612/140F5A32-6.jpg'
        return a.avatar
