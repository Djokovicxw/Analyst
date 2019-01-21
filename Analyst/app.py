from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from pyecharts import Bar, Pie, Liquid, Line
from flask_script import Manager
from flask_moment import Moment
from datetime import datetime
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
    )


@app.route("/data")
def data():
    bar = gen_bar_img()
    line = Line("访问量")
    line.add('', [i for i in range(1, 30)], [random.randint(500,1000) for _ in range (1,30) ])
    return render_template("data.html",
                           echart1=bar.render_embed(),
                           echart2=line.render_embed())


def gen_bar_img():
    db = pymysql.connect(host='localhost', user='qw', password=app.config.get('PASSWORD'), db='7law')
    sql = "select `fullURLId` from `all_gzdata`"
    df = pd.read_sql(sql, db, chunksize=10000)
    counts = [i['fullURLId'].value_counts() for i in df]
    counts = pd.concat(counts).groupby(level=0).sum()
    counts = counts.reset_index()
    counts.columns = ['index', 'num']
    counts['type'] = counts['index'].apply(lambda x: x[:3])
    counts_ = counts[['type', 'num']].groupby('type').sum()
    bar = Bar('页面访问量', '按页面内容分类')
    bar.add('', [i for i in counts_.index], [i[0] for i in counts_.values], is_more_utils=True)
    db.close()
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
