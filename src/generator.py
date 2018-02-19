# coding=utf-8

import json
import requests
from .db import *
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .YDMverify import Yundama


class CookiesGenerator(object):
    """
    cookie生成基类
    """

    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)
        self.init_browser()

    def __del__(self):
        self.close()

    def init_browser(self):
        """
        初始化browser
        :return:
        """
        if BROWSER_TYPE == 'PhantomJS':
            print('使用PhantomJS模拟登录')
            caps = DesiredCapabilities.PHANTOMJS
            caps[
                "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
            self.browser = webdriver.PhantomJS(desired_capabilities=caps)
            self.browser.set_window_size(1400, 500)
        elif BROWSER_TYPE == 'Chrome':
            print('使用chrome模拟登录')
            self.browser = webdriver.Chrome()
        else:
            print('未使用浏览器模拟登录')
            self.browser = None

    @staticmethod
    def process_cookies(cookies):
        """
        处理Cookies
        :param cookies:
        :return:
        """
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie['name']] = cookie['value']
        return cookie_dict

    def new_cookies(self, username, password):
        """
        新生成cookies接口
        :param username: 用户名
        :param password: 密码
        :return:
        """
        raise NotImplementedError

    def run(self):
        """
        启动生成器，得到所有账户，依次模拟登录，需要使用子类重写模拟登录具体方法
        :return:
        """
        accounts_usernames = self.accounts_db.usernames()
        cookies_usernames = self.cookies_db.usernames()

        for username in accounts_usernames:
            if username not in cookies_usernames:
                password = self.accounts_db.get(username)
                result = self.new_cookies(username, password)
                if result:
                    if self.cookies_db.set(username, result):
                        print('成功保存Cookies')
                    else:
                        print('保存失败，请检查数据库')
                else:
                    print('登录失败')
        else:
            print('已获取所有账号Cookies')

    def close(self):
        """
        关闭
        :return:
        """
        try:
            print('Closing Browser')
            self.browser.close()
            del self.browser
        except TypeError:
            print('Browser not opened')


class WeiboCookiesGenerator(CookiesGenerator):
    """
    weibo生成器类，需要重写模拟登录获取cookie部分代码
    """

    def __init__(self, website='weibo'):
        CookiesGenerator.__init__(self, website)
        self.website = website
        self.ydm = Yundama(YUNDAMA_USERNAME, YUNDAMA_PASSWORD, YUNDAMA_APP_ID, YUNDAMA_APP_KEY)

    def new_cookies(self, username, password):
        """
        生成cookies
        :param username:
        :param password:
        :return:
        """
        print('正在生成cookie, 用户名：', username)
        self.browser.delete_all_cookies()
        self.browser.get('http://my.sina.com.cn/profile/unlogin')
        wait = WebDriverWait(self.browser, 20)

        try:
            login = wait.until(EC.visibility_of_element_located((By.ID, 'hd_login')))
            login.click()

            user = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.loginformlist input[name="loginname"]')))
            user.send_keys(username)

            psd = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.loginformlist input[name="password"]')))
            psd.send_keys(password)

            submit = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.login_btn')))
            submit.click()
            try:
                result = self._success(username)
                if result:
                    return result
            except TimeoutException:
                print('出现验证码，开始识别')
                yzm = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.loginform_yzm .yzm')))
                url = yzm.get_attribute('src')
                cookies = self.browser.get_cookies()
                cookies_dict = {}
                for cookie in cookies:
                    cookies_dict[cookie.get('name')] = cookie.get('value')
                response = requests.get(url, cookies=cookies_dict)
                result = self.ydm.identify(stream=response.content)
                if not result:
                    print('验证码识别失败, 跳过识别')
                    return
                door = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '.loginform_yzm input[name="door"]')))
                door.send_keys(result)
                submit.click()
                result = self._success(username)
                if result:
                    return result
        except WebDriverException as e:
            print(e.args)

    def _success(self, username):
        wait = WebDriverWait(self.browser, 5)
        success = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'me_portrait_w')))
        if success:
            self.browser.get('http://weibo.cn/')
            if "我的首页" in self.browser.title:
                print(self.browser.get_cookies())
                cookies = {}
                for cookie in self.browser.get_cookies():
                    cookies[cookie["name"]] = cookie["value"]
                print('成功获取到' + username + 'Cookies')
                return json.dumps(cookies)
