from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from pyecharts import Bar, Pie, Liquid, Line, Geo
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

@app.route("/data_v2")
def data_v2():
    data = [
    ("海门", 9),("鄂尔多斯", 12),("招远", 12),("舟山", 12),("齐齐哈尔", 14),("盐城", 15),
    ("赤峰", 16),("青岛", 18),("乳山", 18),("金昌", 19),("泉州", 21),("莱西", 21),
    ("日照", 21),("胶南", 22),("南通", 23),("拉萨", 24),("云浮", 24),("梅州", 25),
    ("文登", 25),("上海", 25),("攀枝花", 25),("威海", 25),("承德", 25),("厦门", 26),
    ("汕尾", 26),("潮州", 26),("丹东", 27),("太仓", 27),("曲靖", 27),("烟台", 28),
    ("福州", 29),("瓦房店", 30),("即墨", 30),("抚顺", 31),("玉溪", 31),("张家口", 31),
    ("阳泉", 31),("莱州", 32),("湖州", 32),("汕头", 32),("昆山", 33),("宁波", 33),
    ("湛江", 33),("揭阳", 34),("荣成", 34),("连云港", 35),("葫芦岛", 35),("常熟", 36),
    ("东莞", 36),("河源", 36),("淮安", 36),("泰州", 36),("南宁", 37),("营口", 37),
    ("惠州", 37),("江阴", 37),("蓬莱", 37),("韶关", 38),("嘉峪关", 38),("广州", 38),
    ("延安", 38),("太原", 39),("清远", 39),("中山", 39),("昆明", 39),("寿光", 40),
    ("盘锦", 40),("长治", 41),("深圳", 41),("珠海", 42),("宿迁", 43),("咸阳", 43),
    ("铜川", 44),("平度", 44),("佛山", 44),("海口", 44),("江门", 45),("章丘", 45),
    ("肇庆", 46),("大连", 47),("临汾", 47),("吴江", 47),("石嘴山", 49),("沈阳", 50),
    ("苏州", 50),("茂名", 50),("嘉兴", 51),("长春", 51),("胶州", 52),("银川", 52),
    ("张家港", 52),("三门峡", 53),("锦州", 54),("南昌", 54),("柳州", 54),("三亚", 54),
    ("自贡", 56),("吉林", 56),("阳江", 57),("泸州", 57),("西宁", 57),("宜宾", 58),
    ("呼和浩特", 58),("成都", 58),("大同", 58),("镇江", 59),("桂林", 59),("张家界", 59),
    ("宜兴", 59),("北海", 60),("西安", 61),("金坛", 62),("东营", 62),("牡丹江", 63),
    ("遵义", 63),("绍兴", 63),("扬州", 64),("常州", 64),("潍坊", 65),("重庆", 66),
    ("台州", 67),("南京", 67),("滨州", 70),("贵阳", 71),("无锡", 71),("本溪", 71),
    ("克拉玛依", 72),("渭南", 72),("马鞍山", 72),("宝鸡", 72),("焦作", 75),("句容", 75),
    ("北京", 79),("徐州", 79),("衡水", 80),("包头", 80),("绵阳", 80),("乌鲁木齐", 84),
    ("枣庄", 84),("杭州", 84),("淄博", 85),("鞍山", 86),("溧阳", 86),("库尔勒", 86),
    ("安阳", 90),("开封", 90),("济南", 92),("德阳", 93),("温州", 95),("九江", 96),
    ("邯郸", 98),("临安", 99),("兰州", 99),("沧州", 100),("临沂", 103),("南充", 104),
    ("天津", 105),("富阳", 106),("泰安", 112),("诸暨", 112),("郑州", 113),("哈尔滨", 114),
    ("聊城", 116),("芜湖", 117),("唐山", 119),("平顶山", 119),("邢台", 119),("德州", 120),
    ("济宁", 120),("荆州", 127),("宜昌", 130),("义乌", 132),("丽水", 133),("洛阳", 134),
    ("秦皇岛", 136),("株洲", 143),("石家庄", 147),("莱芜", 148),("常德", 152),("保定", 153),
    ("湘潭", 154),("金华", 157),("岳阳", 169),("长沙", 175),("衢州", 177),("廊坊", 193),
    ("菏泽", 194),("合肥", 229),("武汉", 273),("大庆", 279)]
    geo = Geo(
        "用户区域分布图",
        "data from Analyst",
        title_color="#fff",
        title_pos="center",
        width=1200,
        height=600,
        background_color="#404a59",
    )
    attr, value = geo.cast(data)
    geo.add(
        "",
        attr,
        value,
        visual_range=[0, 200],
        visual_text_color="#fff",
        symbol_size=15,
        is_visualmap=True,
    )
    line = Line("总访问量")
    line.add('', [i for i in range(1, 30)], [random.randint(500,1000) for _ in range (1,30) ])
    dict1 = ['访问主页', '注册', '购买商品', '售后询问', '技术咨询', '访问论坛', '其他']
    dict2 = [900, 142, 134, 111, 300, 512, 567]
    pie = gen_pie_img("具体行为", dict1, dict2, "Last Week", True )
    return render_template("data-v2.html", 
                            echart1=pie.render_embed(), 
                            echart2=line.render_embed(), 
                            echart3=geo.render_embed(),
                            script_list=geo.get_js_dependencies())


@app.route("/data")
def data():
    bar = gen_bar_img()
    line = Line("总访问量")
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
    bar.add('', [i for i in counts_.index], [i[0] for i in counts_.values])
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
