from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from pyecharts import Bar, Pie
from flask_script import Manager
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
Bootstrap = Bootstrap(app)
momentt = Moment(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login_in():
    return render_template("login.html")


@app.route("/UserProfile")
def UserProfile():
    bar = gen_bar_img()
    pie = gen_pie_img()
    return render_template("UserProfile.html",
        echart1=bar.render_embed(),
        echart2=pie.render_embed(),
        current_time = datetime.utcnow() 
    )


@app.route("/data")
def data():
    bar = gen_bar_img()
    pie = gen_pie_img()
    return render_template("data.html",
                           echart1=bar.render_embed(),
                           echart2=pie.render_embed())


def gen_bar_img():
    bar = Bar("Last Week")
    bar.add("用户点击量", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            [100, 200, 134, 111, 300, 512, 567], mark_line=["average"], mark_point=["max"])
    return bar


def gen_pie_img():
    pie = Pie("Last Week")
    pie.add("用户点击量", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            [100, 200, 134, 111, 300, 512, 567], is_label_show=True)
    return pie


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)