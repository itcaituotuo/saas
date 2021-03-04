# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2020/12/4 15:09

from django.conf.urls import url

from web.views import account
from web.views import home
from web.views import project
from web.views import static

# url/路由 管理
urlpatterns = [
    # 第一期：用户认证相关（用户注册（短信验证码、图片验证码）、验证码登录、用户名密码登录、退出登录）
    url(r'^send/sms/$', account.send_sms, name='send_sms'),  # 发送短信验证码
    url(r'^register/$', account.register, name='register'),  # 注册

    url(r'^login/sms/$', account.login_sms, name='login_sms'),  # 验证码登录

    url(r'^login/$', account.login, name='login'),  # 用户名和密码登录
    url(r'^image/code/$', account.image_code, name='image_code'),  # 图片验证码

    url(r'^index/$', home.index, name='index'),  # 主页

    url(r'^logout/$', account.logout, name='logout'),  # 退出登录

    # 第二期：项目管理
    url(r'^project/list/$', project.project_list, name='project_list'),  # 项目列表展示

    url(r'^price/$', static.price, name='price'),  # 项目列表展示

]
