from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import session
from routes.user import User
from models.weibo import Weibo,Comment


def current_user():
    uid = session.get("user_id")
    if uid is not None:
        u = User.query.get(uid)
        return u
main = Blueprint('weibo', __name__)


@main.route('/weibo')
def index():
    u = current_user()
    if u is None:
        return redirect(url_for('/'))
    weibo_list = Weibo.query.order_by(Weibo.id.desc()).all()
    for i in weibo_list:
        comment_list = i.comments()
        print('commetlist',comment_list)
        for j in comment_list:
            u = User.query.filter_by(id=j.user_id).first()
            if u is not None:
                print('u',u.username,u.password)
                j.avatar = u.avatar
                print('tt头像',j.avatar)
            else:
                j.avatar = 'http://k1.jsqq.net/uploads/allimg/1612/140F5A32-6.jpg'
        u = User.query.filter_by(id=i.user_id).first()
        i.comments_num = len(i.comments())
        i.avatar = i.get_avatar()
    return render_template('weibo_index.html', weibos=weibo_list, user_id=u.id)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    u = current_user()
    t = Weibo(form)
    t.name = u.username
    if t.valid():
        t.save()
    return redirect(url_for('.index'))


@main.route('/comment', methods=['POST'])
def comment():
    form = request.form
    u = current_user()
    c = Comment(form)
    print('request comment',c.comment)
    c.name = u.username
    if c.valid():
        c.save()
    return redirect(url_for('.index'))


@main.route('/delete/<int:weibo_id>')
def delete(weibo_id):
    w = Weibo.query.get(weibo_id)
    w.delete()
    return redirect(url_for('.index'))
