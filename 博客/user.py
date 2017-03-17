from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import abort
from flask import session

from models import User


# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字，第二个参数是套路
main = Blueprint('user', __name__)


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


@main.route('/')
def login_view():
    u = current_user()
    if u is not None:
        return redirect('/blog')
    else:
        return render_template('user_login.html')


@main.route('/user/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    if u.valid():
        u.save()
    else:
        abort(400)
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
    return redirect(url_for('.login_view'))


@main.route('/user/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    # 检查 u 是否存在于数据库中并且 密码用户 都验证合格
    user = User.query.filter_by(username=u.username).first()
    if user is not None and user.validate_login(u):
        print('登录成功')
        session['user_id'] = user.id
    else:
        print('登录失败')
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
    return redirect(url_for('.login_view'))

@main.route('/user/profile')
def user_profile():
    u = current_user()
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
    return render_template('user_profile.html',u=u)

@main.route('/user/update', methods=['POST'])
def user_update():
    form = request.form
    u=current_user()
    u.password=form.get('password','')
    u.save()

    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
    return redirect(url_for('.user_profile'))
