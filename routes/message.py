from models.blog import Blog
from routes import *

from models.message import Message

Model = Message

main = Blueprint('msg', __name__)


@main.route('/message')
def index():
    # 查找所有的 msg 并返回
    msgs = Model.query.all()
    # print('msg index', msgs, len(msgs))
    return render_template('message.html', msgs=msgs)


@main.route('/msg/add', methods=['POST'])
def add():
    form = request.form
    Message.new(form)
    return redirect(url_for('.index'))
