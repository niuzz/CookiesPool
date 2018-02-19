# coding=utf-8
import random
import redis
from .config import *


class RedisClient(object):
    """
    redis操作类
    dbtype 是账号类型还是cookies类型等
    """
    def __init__(self, dbtype, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.type = dbtype
        self.website = website

    def name(self):
        """
        哈希名称
        :return:
        """
        return "{type}:{website}".format(type=self.type, website=self.website)

    def set(self, username, value):
        """
        设置键值对
        :param username:
        :param value:
        :return:
        """
        return self.db.hset(self.name(), username, value)

    def get(self, username):
        """
        根据键名取键值
        :param username:
        :return:
        """
        return self.db.hget(self.name(), username)

    def delete(self, username):
        """
        根据键名删除键值
        :param username:
        :return:
        """
        return self.db.hdel(self.name(), username)

    def count(self):
        """
        获取条数
        :return:
        """
        return self.db.hlen(self.name())

    def random(self):
        """
        随机取的键值
        :return:
        """
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        """
        获取所有账户信息
        :return:
        """
        return self.db.hkeys(self.name())

    def all(self):
        """
        获取所有键值对
        :return:
        """
        return self.db.hgetall(self.name())
