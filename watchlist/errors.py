from watchlist import app
from flask import render_template

# 创建错误处理函数，相当于错误页面的视图函数
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404