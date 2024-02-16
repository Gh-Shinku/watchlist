from flask import Flask, render_template
from flask import url_for
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import os, sys
import click

# 创建应用实例
app = Flask(__name__)
# 创建数据库
db = SQLAlchemy(app)

# 创建路由及对应的视图函数
@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies = movies)

@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    return 'Test Page'

# 创建错误处理函数，相当于错误页面的视图函数
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 创建模板上下文处理函数
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user = user)

# 创建两个模型类，其实就是建表，关键在于继承了db.Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

# 不同系统之间的兼容性
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')
'''
db.create_all()
user = User(name='Grey Li')  # 创建一个 User 记录
m1 = Movie(title='Leon', year='1994')  # 创建一个 Movie 记录
m2 = Movie(title='Mahjong', year='1996')  # 再创建一个 Movie 记录
db.session.add(user)  # 把新创建的记录添加到数据库会话
db.session.add(m1)
db.session.add(m2)
db.session.commit()  # 提交数据库会话，只需要在最后调用一次即可
'''