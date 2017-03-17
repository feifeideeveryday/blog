from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import abort
from flask import session


from models import Blog
from models import User
from models import Comment

# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字，第二个参数是套路
main = Blueprint('blog', __name__)


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u

@main.route('/blog')
def blog_view( ):
    u = current_user()
    if u is None:
        abort(404)
    else:
        # ws = Weibo.query.filter_by(user_id=u.id).all()
        # 用函数的方法在model中处理这个过程只要写清楚函数的就可以
        bs = u.blogs()
        for b in bs:
           b.load_comments()
        return render_template('blog_index.html',blogs=bs)


@main.route('/blog/add', methods=['POST'])
def add():
    u = current_user()
    if u is not None:
        print('blog add', u.id, u.username, u.password)
        form = request.form
        b = Blog(form)
        b.user_id = u.id
        b.save()
        print('boke task',b.task)
        return redirect(url_for('blog.blog_view', username=u.username))
    else:
        abort(401)

@main.route('/blog/add/path')
def blog_add_path():
    return  render_template('blog_add.html')

@main.route('/comment/add', methods=['POST'])
def comment_add():
    u = current_user()
    if u is not None:
        form = request.form
        c = Comment(form)
        c.user_id = u.id
        c.blog_id = int(form.get('blog_id', -1))
        c.save()
        return redirect(url_for('blog.blog_view', username=u.username))
    else:
        abort(401)
