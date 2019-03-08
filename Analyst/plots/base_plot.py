import pandas as pd
from pyecharts import Bar
import pymysql
from Analyst.settings import DbConnect as db


def db_iter(sql: str, size: int = 10000):
    """
    sql到pd分块读取
    :param sql: sql query
    :param size: chunksize
    :return:
    """
    con = pymysql.connect(host=db.host, user=db.user, password=db.pswd, db=db.db)
    gener = pd.read_sql_query(sql, con, chunksize=size)
    con.close()
    return gener


def gp_plot(sql: str, fg_title: str = '', fg_sub_title: str = '', mid_func = lambda x: x):
    """
    对数据库中的一列进行分类统计，返回html
    :param sql: 对象列的sql查询
    :param fg_title: 图标题
    :param fg_sub_title: 图副标题
    :param mid_func: 对数据进行处理的函数
    :return:
    """
    gener = db_iter(sql)
    counts = [i.iloc[:, 0].dropna().apply(mid_func).value_counts() for i in gener]
    counts = pd.concat(counts).groupby(level=0).sum()
    counts = counts.reset_index()
    counts.columns = ['index', 'num']
    bar = Bar(fg_title, fg_sub_title)
    bar.add('', [i for i in counts['index']], [i[1] for i in counts.values], is_more_utils=True)
    return bar.render_embed(), bar.get_js_dependencies()


def visit_time(time_row: str, sql: str):
    """
    访问时间统计函数
    :param time_row: 时间列
    :param sql: 时间列的sql语句，非字符型的需要使用sql函数转换 eg："2015-02-03 22:21:08"
    :return:
    """
    gener = db_iter(sql)
    counts = [pd.to_datetime(i[time_row]).apply(lambda x: x.hour).value_counts() for i in gener]
    counts = pd.concat(counts).groupby(level=0).sum()
    counts = counts.reset_index()
    counts.columns = ['dex', 'num']
    bar = Bar('访问时间统计')
    bar.add('', counts.dex, list(counts.num), is_more_utils=True, is_datazoom_show=True)
    return bar.render_embed(), bar.get_js_dependencies()


def visit_days(date_row: str, sql: str):
    gener = db_iter(sql)
    counts = [pd.to_datetime(i[date_row]).apply(lambda x: x.day).value_counts() for i in gener]
    counts = pd.concat(counts).groupby(level=0).sum()
    counts = counts.reset_index()
    counts.columns = ['dex', 'num']
    bar = Bar('月访问情况统计')
    bar.add('', counts.dex, list(counts.num), is_more_utils=True, is_datazoom_show=True)
    return bar.render_embed(), bar.get_js_dependencies()


def refer_ana():
    pass
# todo 完成来源分析函数


if __name__ == "__main__":
    pass
