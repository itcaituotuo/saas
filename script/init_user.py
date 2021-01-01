# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2020/12/9 14:19

# django离线脚本

import django
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saas.settings")
django.setup()

from web import models

# 往数据库添加数据，连接数据库、操作、关闭链接
models.UserInfo.objects.create(username='蔡', email='12345678@qq.com', mobile_phone='15059224499', password='12345678')
