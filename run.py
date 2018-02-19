# coding=utf-8
from src.scheduler import Scheduler


def main():
    """
    调度器入口
    :return:
    """
    s = Scheduler()
    s.run()
    print('------------------------------------>')
    print('欢迎使用nj_cookies_pool, 调度器开始运行……')
    print('------------------------------------>')


if __name__ == '__main__':
    main()
