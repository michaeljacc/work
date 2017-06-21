from models.blog import Blog
from models.user import User
from routes import *

main = Blueprint('Blog', __name__)

Model = Blog

def current_user():
    uid = session.get("user_id")
    if uid is not None:
        u = User.query.get(uid)
        return u

@main.route('/blogs')
def index():
    ms = Model.query.all()
    u = current_user()
    return render_template('blog_list.html', blog_list=ms, user_id=u.id)


@main.route('/blogs/new')
def new():
    return render_template('blog_new.html')


@main.route('/blogs/add', methods=['POST'])
def add():
    form = request.form
    Blog.new(form)
    return redirect(url_for('.index'))


@main.route('/blogs/<int:blog_id>')
def detail(blog_id):
    b = Blog.query.get(blog_id)
    cs = Comment.query.filter_by(blog_id=b.id).all()
    return render_template('blog_detail.html', blog=b, comments=cs)


@main.route('/blogs/blogs')
def blog():
    u =current_user()
    ms = Model.query.all()
    return render_template('blog_all.html', blog_list=ms,user_id=u.id)


@main.route('/comment/add', methods=['POST'])
def add_comment():
    form = request.form
    print('add comment', form)
    c = Comment.new(form)
    # url_for 的第二个参数可以匹配到动态路由
    # /blog/<c.blog_id>
    # 如果没有动态路由，参数就变成 query 的形式
    # /blog/new?blog_id=1
    return redirect(url_for('.detail', blog_id=c.blog_id))
    # return redirect('/blog/{}'.format(c.blog_id))
