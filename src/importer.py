# coding=utf-8

from .db import RedisClient

conn = RedisClient('accounts', 'weibo')


def save_to_redis(account, sep='----'):
    """
    写入redis
    :param account:
    :param sep:
    :return:
    """
    username, password = account.split(sep)
    result = conn.set(username, password)
    print('账号', username, '密码', password)
    print('写入成功' if result else '写入失败')


def scan():
    """
    扫描文件，准备写入redis
    :return:
    """
    with open('weibo1-20.txt') as f:
        # 按行读取
        for line in f:
            save_to_redis(line)


if __name__ == '__main__':
    scan()
