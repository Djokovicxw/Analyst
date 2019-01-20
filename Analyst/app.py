from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from pyecharts import Bar, Pie
from flask_script import Manager
from flask_moment import Moment
from datetime import datetime
import pymysql

app = Flask(__name__)
app.config.from_pyfile('default_config.py')
Bootstrap = Bootstrap(app)
moment = Moment(app)


    @app.route("/")
    def index():
        con = pymysql.connect(host='localhost',user='qw', password=app.config.get('PASSWORD'), db='mysql')
        cur = con.cursor()
        sql = "SELECT `user` from `user`"
        cur.execute(sql)
        res = cur.fetchall()
        return render_template("index.html", user=res)


@app.route("/login")
def login_in():
    return render_template("login.html")


@app.route("/UserProfile")
def UserProfile():
    bar = gen_bar_img()
    dict1 = ['访问主页', '注册', '购买商品', '售后询问', '技术咨询', '访问论坛', '其他']
    dict2 = [900, 142, 134, 111, 300, 512, 567]
    pie = gen_pie_img("具体行为", dict1, dict2, "Last Week", True )
    return render_template("UserProfile.html",
        echart1=bar.render_embed(),
        echart2=pie.render_embed(),
        current_time = datetime.utcnow() 
    )


@app.route("/data")
def data():
    bar = gen_bar_img()
    dict1 = ['访问主页', '注册', '购买商品', '售后询问', '技术咨询', '访问论坛', '其他']
    dict2 = [900, 142, 134, 111, 300, 512, 567]
    pie = gen_pie_img("行为统计", dict1, dict2, "Last Week", True )
    return render_template("data.html",
                           echart1=bar.render_embed(),
                           echart2=pie.render_embed())


def gen_bar_img():
    bar = Bar("Last Week")
    bar.add("用户点击量", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            [100, 200, 134, 111, 300, 512, 567], mark_line=["average"], mark_point=["max"])
    return bar


def gen_pie_img(name, dict1, dict2, title="title", flag=True):
    pie = Pie(title)
    pie.add(name, dict1, dict2, is_label_show=flag)
    return pie


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
