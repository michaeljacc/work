from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import abort
from flask import session

from models.user import User

main_user = Blueprint('user', __name__)


def current_user():
    uid = session.get("user_id")
    if uid is not None:
        u = User.query.get(uid)
        return u


@main_user.route('/')
def login_view():
    u = current_user()
    if u is not None:
        return redirect('/blogs')
    else:
        return render_template('test.html')


@main_user.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    avatar = u.av()
    u.avatar = avatar
    if u.valid():
        u.save()
    else:
        abort(410)
    return redirect(url_for('.login_view'))


@main_user.route('/login', methods=['POST'])
def login():
    form = request.form
    print("form", form)
    u = User(form)
    user = User.query.filter_by(username=u.username).first()
    if user is not None and user.validate_login(u):
        print("success")
        session['user_id'] = user.id
    else:
        print('FAILD')
        return redirect(url_for('.login_view'))
    return redirect("/blogs")


@main_user.route('/detail', methods=['GET'])
def detail():
    u = current_user()
    print('u', u.avatar)
    u.avatar = '/static/images/avatar (12).jpg'
    print('u', u.avatar)
    return render_template('detail.html', user=u)
