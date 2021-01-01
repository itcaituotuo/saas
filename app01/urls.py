# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2020/12/4 15:06


from django.conf.urls import url
from app01 import views

urlpatterns = [
    url(r'^send/sms', views.send_sms),
    url(r'^register', views.register, name='register'),  # 反向解析"app01:register"
]
