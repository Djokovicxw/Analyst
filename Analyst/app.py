from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from pyecharts import Bar, Pie, Liquid, Line
from flask_script import Manager
from flask_moment import Moment
from datetime import datetime
from models.base_plot import *
import pymysql
import numpy as np 
import pandas as pd 
import random

app = Flask(__name__)
app.config.from_pyfile('default_config.py')
Bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=['POST', 'GET'])
def login_in():
    if request.method == 'POST':
        name = request.form['username']
        pwd = request.form['pwd']
        if name == 'admin' and pwd == 'analyst':
            return redirect(url_for('data'))
    else:
        return render_template("login.html")


@app.route("/data", methods=['POST', 'GET'])
def data():
    dict1 = ['访问主页', '注册', '购买商品', '售后询问', '技术咨询', '访问论坛', '其他']
    dict2 = [900, 142, 134, 111, 300, 512, 567]
    bar = gen_pie_img("具体行为", dict1, dict2, "Last Week", True)
    line = Line("访问量")
    line.add('', [i for i in range(1, 30)], [random.randint(500,1000) for _ in range (1,30) ])
    return render_template("data_v2.html",
                           echart1=bar.render_embed(),
                           echart2=line.render_embed())


def gen_pie_img(name, dict1, dict2, title="title", flag=True):
    pie = Pie(title)
    pie.add(name, dict1, dict2, is_label_show=flag)
    return pie


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
