## 基于redis, Python3.6实现的可扩展cookies池
### --->>> 内建了新浪微博模拟登录，配合云打码API完成校验码识别
### 基于静觅cookiesPool实现，优化了redis相关操作
1.批量导入账号, 直接按行导入文件weibo1-20.txt内包含的账号
```bash
python3 importer.py
```
2.设置config

```python
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
```

3.配置模块开关，在config.py文件内设置
```python
# 验证器开关，检测redis中的Cookies是否可用，不可用删除
VALID_PROCESS = False

# API接口服务开关
API_PROCESS = False

# 生产器开关，从redis读取账号密码，进行模拟登录，如果登录成功将cookie存入redis
GENERATOR_PROCESS = True
```
4.启动cookie池
```bash
python3 run.py
```
todo: 使用RSA加密绕过验证直接登录微博