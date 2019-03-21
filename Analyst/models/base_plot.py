import pandas as pd
import re
import pymysql
from settings import DbConnect as db
from user_agents import parse
from datetime import datetime


def db_iter(sql: str, size: int = 10000):
    """
    sql到pd分块读取
    :param sql: sql query
    :param size: chunksize
    :return:
    """
    con = pymysql.connect(host=db.host, user=db.user, password=db.pwd, db=db.db)
    gener = pd.read_sql_query(sql, con, chunksize=size)
    con.close()
    return gener


def gp_plot(sql: str, mid_func=lambda x: x):
    """
    对数据库中的对值进行计数
    :param sql: 对象列的sql查询
    :param mid_func: 对数据值进行计数前的处理函数，符合pandas.apply()函数要求
    :return: x, y
    """
    gener = db_iter(sql)
    counts = [i.iloc[:, 0].dropna().apply(mid_func).value_counts() for i in gener]
    counts = pd.concat(counts).groupby(level=0).sum()
    counts = counts.reset_index()
    return [i for i in counts['index']], [i[1] for i in counts.values]


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
    return counts.dex, list(counts.num)


def visit_days(date_row: str, sql: str):
    """
    统计一个月内
    :param date_row:
    :param sql:
    :return:
    """
    gener = db_iter(sql)
    counts = [pd.to_datetime(i[date_row]).apply(lambda x: x.day).value_counts() for i in gener]
    counts = pd.concat(counts).groupby(level=0).sum()
    counts = counts.reset_index()
    return counts.dex, list(counts.num)


def refer_ana(refer_row: str, sql: str):
    """
    来源域名分析
    :param refer_row: 来源域名列名
    :param sql: 读取数据库的sql
    :return:
    """
    def get_domain(url):
        re_res = re.search(r'(\w+\.)?(\w+)\.(com|cn|net|org|gov)', url)
        if re_res:
            return re_res.group(2)
        else:
            return None
    gener = db_iter(sql)
    counts = [i[refer_row].dropna().apply(get_domain).value_counts() for i in gener]
    counts = pd.concat(counts).groupby(level=0).sum()
    counts = counts.reset_index()
    counts.columns = ['dex', 'num']
    counts = counts[counts.num > 100].sort_values('num', ascending=False)
    return counts.dex, list(counts.num)


def ua_ana(ua_row: str, sql: str):
    """
    对user_agent进行分析，包括操作系统，终端设备
    :param ua_row: user_agent列名
    :param sql: sql语句
    :return: 返回os与，device的统计信息
    """
    gener = db_iter(sql)
    ua_parse = [i[ua_row].dropna().apply(lambda x: parse(x)) for i in gener]
    device = [i.apply(lambda x: x.device.brand).value_counts() for i in ua_parse]
    device = pd.concat(device).groupby(level=0).sum()
    os_info = [i.apply(lambda x: x.os.family).value_counts() for i in ua_parse]
    os_info = pd.concat(os_info).groupby(level=0).sum()
    return (device.index, list(device.values)), (os_info.index, list(os_info.values))


def actvt_user(user_id_row: str, time_row: str, sql: str, ac_type: str, date_str_format="%Y-%m-%d %H:%M:%S"):
    """
    统计sql选取的用户数量，统计日活跃则传入某天的用户数, 月活则传入一月的sql
    :param user_id_row: 用户id列名
    :param time_row: 时间列名
    :param sql: 读数据的sql
    :param ac_type: 可选‘day’, 或'month'
    :param date_str_format:
    :return: 用户数
    """
    gener = db_iter(sql)
    if ac_type == 'day':
        user = [pd.DataFrame(
            {'date': pd.to_datetime(i[time_row], format=date_str_format).apply(lambda x: x.date()),
            'id': i[user_id_row]}) for i in gener]
    elif ac_type == 'month':
        user = [pd.DataFrame(
            {'date': pd.to_datetime(i[time_row], format=date_str_format).apply(lambda x: x.month()),
            'id': i[user_id_row]}) for i in gener]
    user = [i.drop_duplicates().groupby('date').count() for i in user]
    return pd.concat(user).groupby('date').sum()


def lost_user(user_id_row: str, time_row: str, sql: str, offline_limit=5, date_str_format="%Y-%m-%d %H:%M:%S"):
    """
    计算沉默用户比例
    计算最后使用与当前日期的相差的天数，大于指定的界限即认为沉默
    :param user_id_row: 用户id列名
    :param time_row: 时间列名
    :param sql: 读数据的sql
    :param offline_limit: 离线判定天数
    :param date_str_format: 日期字符串格式
    :return: 沉默用户数
    """
    gener = db_iter(sql)
    delta_from_now = [datetime(2015, 5, 1) - pd.DataFrame({'id':i[user_id_row], 'time':pd.to_datetime(i[time_row],
                                                      format=date_str_format)}).groupby('id').max() for i in gener]
    delta_from_now = [i.time.apply(lambda x: x.days) for i in delta_from_now]
    delta_from_now = pd.concat(delta_from_now) 
    return delta_from_now[delta_from_now > offline_limit].count()


if __name__ == "__main__":
    pass
