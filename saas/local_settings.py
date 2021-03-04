# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2020/12/2 19:06

LANGUAGE_CODE = 'zh-hans'

SMS = 666

# sms配置
# 腾讯云短信应用的 app_id
TENCENT_SMS_APP_ID = 1400457131

# 腾讯云短信应用的 app_key
TENCENT_SMS_APP_KEY = "7fb77cfb6db238c7ddadde1435b94d52"

# 腾讯云短信签名内容
TENCENT_SMS_SIGN = "IT小学生蔡坨坨"

# django-redis相关配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",  # 安装redis的主机的 IP 和 端口
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            # "PASSWORD": "foobared" # redis密码
        }
    }
}
