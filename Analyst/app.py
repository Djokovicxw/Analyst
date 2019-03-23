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
    dict1 = ['访问主页','注册', '购买商品', '售后询问', '技术咨询', '访问论坛', '其他']
    dict2 = [900, 142, 134, 111, 300, 512, 567]
    pie = Pie("用户行为")
    pie.add("具体行为", dict1, dict2)
    line = Line('访问量')
    sql = "select timestamp_format from all_gzdata"
    x_dict, y_dict = visit_time('timestamp_format', sql)
    line.add('每个时段的访问量',x_dict, y_dict)
    bar = Bar("每月访问天数")
    x_dict, y_dict = visit_days('timestamp_format', sql)
    bar.add('统计一个月每天的平均访问量', x_dict, y_dict, xaxis_name="号", yaxis_name="次数", xaxis_name_pos='end',yaxis_name_pos='end')
    sql = "select userID,ymd from all_gzdata"
    lostUser = lost_user('userID', 'ymd', sql, offline_limit=15)
    alluser = db_sql('select count(*) from all_gzdata')
    liquid = Liquid("客户损失量")
    liquid.add('超过5天未访问页面为沉默用户', [lostUser / alluser])

    ## 来源统计Pie图
    pie2 = Pie("来源统计")
    sql = "select fullReferrerURL from all_gzdata" 
    x_dict, y_dict = refer_ana('fullReferrerURL', sql)
    pie2.add('Reffer URL', x_dict, y_dict)
    return render_template("data.html",
                           echart1=line.render_embed(),
                           echart2=pie.render_embed(),
                           echart3=bar.render_embed(),
                           echart4=pie2.render_embed())


@app.route("/user")
def user():
    sql = "select userID,ymd from all_gzdata"
    lostUser = lost_user('userID', 'ymd', sql, offline_limit=15)
    alluser = db_sql('select count(*) from all_gzdata')
    liquid1 = Liquid("客户损失量")
    liquid1.add('超过5天未访问页面为沉默用户', [lostUser / alluser])
    sql = "select userID, timestamp_format from all_gzdata where timestamp_format like '2015-02-03%'"
    actUser = actvt_user('userID', 'timestamp_format', sql, 'day')
    liquid2 = Liquid('活跃用户量')
    liquid2.add('五天内访问过页面的用户', [actUser / alluser])
    sql = "select userAgent from all_gzdata"
    de_dict, de_ydict, os_dict, os_ydict = ua_ana('userAgent', sql)
    pie1 = Pie("用户使用的设备")
    pie1.add("具体设备", de_dict, de_ydict)
    pie2 = Pie('用户使用的操作系统')
    pie2.add('操作系统', os_dict, os_ydict)
    return render_template('user,html', echart1=liquid1.render_embed(),
                                        echart2=liquid2.render_embed(),
                                        echart3=pie1.render_embed(),
                                        echart4=pie2.render_embed(),
                                        script_list=liquid1.get_js_dependencies())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
