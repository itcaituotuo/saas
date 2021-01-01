# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2020/12/4 10:55

import redis


# # 方法一：直接连接redis
# conn = redis.Redis(host='127.0.0.1', port=6379, encoding='utf-8')
# # 设置键值：15059224492="2222" 且超时时间为60秒（值写入到redis时会自动转字符串）
# conn.set('15059224492', 2222, ex=60)
# # 根据键获取值：如果存在获取值（获取到的是字节类型）；不存在则返回None
# value = conn.get('15059224492')
# print(value)

from django.shortcuts import HttpResponse
from django_redis import get_redis_connection

# 方法二：创建redis连接池
pool = redis.ConnectionPool(host='127.0.0.1',
                            port=6379,
                            encoding='utf-8',
                            max_connections=1000)
# 去连接池中获取一个连接
conn = redis.Redis(connection_pool=pool)

conn.set('15059224492', 9986, ex=60)
# 根据键获取值：如果存在获取值（获取到的是字节类型）；不存在则返回None
value = conn.get('15059224492')
print(value)
