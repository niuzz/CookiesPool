# coding=utf-8
import json
import requests
from requests.exceptions import ConnectionError
from .db import *


class ValidTester(object):
    """
    测试cookie类
    """

    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)

    def test(self, username, cookies):
        """
        定义子类测试cookie有效性接口
        :param username:
        :param cookies:
        :return:
        """
        raise NotImplementedError

    def run(self):
        """
        测试类运行接口
        :return:
        """
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)


class WeiboValidTester(ValidTester):
    """
    微博测试子类
    """

    def __init__(self, website='weibo'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        """
        测试接口子类实现
        :param username:
        :param cookies:
        :return:
        """
        print('正在测试Cookies', '用户名', username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies格式错误', username)
            self.cookies_db.delete(username)
            print('删除Cookies', username)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url, cookies=cookies, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                print('Cookies有效', username)
            else:
                print(response.status_code, response.headers)
                print('Cookies失效', username)
                self.cookies_db.delete(username)
                print('删除Cookies', username)

        except ConnectionError as e:
            print('测试异常中断', e.args)

