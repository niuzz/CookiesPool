# coding=utf-8
# Redis数据库地址
REDIS_HOST = 'localhost'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

# 云打码配置
YUNDAMA_USERNAME = ''  # 填入云打码相应账号密码
YUNDAMA_PASSWORD = ''
YUNDAMA_APP_ID = '4524'
YUNDAMA_APP_KEY = '7b4d41f0d075cf9f70d9bca4bdc3309f'

YUNDAMA_API_URL = 'http://api.yundama.com/api.php'

# 云打码最大尝试次数
YUNDAMA_MAX_RETRY = 20

# 循环周期
CYCLE = 120

# 生产器配置的浏览器
# BROWSER_TYPE = 'Chrome'
BROWSER_TYPE = 'PhantomJS'

# 生产器类配置
GENERATOR_MAP = {
    'weibo': 'WeiboCookiesGenerator'
}

# 检测器类
TESTER_MAP = {
    'weibo': 'WeiboValidTester'
}

TEST_URL_MAP = {
    'weibo': 'https://m.weibo.cn/'
}

# API接口服务器地址端口
API_HOST = '127.0.0.1'
API_PORT = 5000

# 验证器开关，检测redis中的Cookies是否可用，不可用删除
VALID_PROCESS = False

# API接口服务开关
API_PROCESS = False

# 生产器开关，从redis读取账号密码，进行模拟登录，如果登录成功将cookie存入redis
GENERATOR_PROCESS = True
