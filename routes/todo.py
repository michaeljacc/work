from models.todo import Todo
from routes import *
from models.user import User
from routes.user import main_user

main = Blueprint('todo', __name__)

Model = Todo

def current_user():
    uid = session.get("user_id")
    if uid is not None:
        u = User.query.get(uid)
        return u

@main.route('/<int:user_id>')
def index(user_id):
    todo_user = User.query.get(user_id)
    print('1111', todo_user)
    ms = todo_user.todos()
    print('1111', ms)
    return render_template('todo_index.html', todo_list=ms)



@main.route('/edit/<id>')
def edit(id):
    m = Model.query.get(id)
    return render_template('todo_edit.html', todo=m)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    u = current_user()
    if u is None:
        return redirect(url_for('/'))
    t = Todo(form)
    t.user_id = u.id
    t.save()
    print(u,t,u.id)
    return redirect(url_for('.index', user_id=u.id))


@main.route('/update/<id>', methods=['POST'])
def update(id):
    form = request.form
    print('form update', form)
    t = Todo.query.get(id)
    t.update(form)
    u = current_user()
    return redirect(url_for('.index', user_id = u.id))

@main.route('/complete/<id>')
def complete(id):
    u = current_user()
    t = Todo.query.get(id)
    if u.id != t.user_id:
        print('完成别人的todo')
        return redirect(url_for('.index', user_id = u.id))
    else :
        t.complete = True
        t.save()
        return redirect(url_for('.index', user_id = u.id))


@main.route('/delete/<id>')
def delete(id):
    Model.delete(id)
    u = current_user()
    return redirect(url_for('.index', user_id = u.id))
