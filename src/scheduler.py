# coding=utf-8
import time
from multiprocessing import Process
from .tester import *
from .generator import *
from .api import *
from .config import *


class Scheduler(object):
    """
    中心调度类
    """

    @staticmethod
    def generate_cookie(cycle=CYCLE):
        """
        生产cookies
        :param cycle:
        :return:
        """
        while True:
            print('Cookies生产进程开始运行')
            try:
                for website, cls in GENERATOR_MAP.items():
                    generator = eval(cls + '(website="' + website + '")')
                    generator.run()
                    print('Cookies生产完成')
                    generator.close()
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def valid_cookie(cycle=CYCLE):
        """
        检测cookies
        :param cycle:
        :return:
        """
        while True:
            print('Cookies检测进程开始运行')
            try:
                for website, cls in TESTER_MAP.items():
                    tester = eval(cls + '(website="' + website + '")')
                    tester.run()
                    print('Cookies检测完成')
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print('异常中断', e.args)

    @staticmethod
    def api():
        """
        API接口
        :return:
        """
        print('API接口开始运行')
        app.run(host=API_HOST, port=API_PORT)

    @staticmethod
    def run():
        """
        中心调度启动
        :return:
        """
        if VALID_PROCESS:
            valid_process = Process(target=Scheduler.valid_cookie)
            valid_process.start()

        if API_PROCESS:
            api_process = Process(target=Scheduler.api)
            api_process.start()

        if GENERATOR_PROCESS:
            generator_process = Process(target=Scheduler.generate_cookie)
            generator_process.start()
            # Scheduler.generate_cookie(120)
