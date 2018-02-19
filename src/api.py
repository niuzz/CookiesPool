# coding=utf-8
import json
from flask import Flask, g
from .config import *
from .db import *

__all__ = ['app']

app = Flask(__name__)


@app.route('/')
def index():
    """
    API入口界面
    :return:
    """
    return '<h3>This is nj Cookie Pool System</h3>'


def get_conn():
    """
    获取连接
    :return:
    """
    for website in GENERATOR_MAP:
        print(website)
        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient' + '("cookies", "' + website + '")'))
            setattr(g, website + '_accounts', eval('RedisClient' + '("accounts", "' + website + '")'))
    return g


@app.route('/<website>/random')
def random(website):
    """
    取随机Cookies数据
    :param website:
    :return:
    """
    g_obj = get_conn()
    cookies = getattr(g_obj, website + '_cookies').random()
    return cookies


@app.route('/<website>/count')
def count(website):
    """
    获取相应站点对应的cookies总数
    :param website:
    :return:
    """
    g_obj = get_conn()
    cookies_count = getattr(g_obj, website + '_cookies').count()
    return json.dumps({'status': '1', 'count': cookies_count})
