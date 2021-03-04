# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2020/12/8 23:05

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from web import models
from django.conf import settings


# 中间件
class AuthMiddleware(MiddlewareMixin):
    """  自定义中间件 """

    def process_request(self, request):
        """  如果用户已登录，则request中赋值 """

        # 获取user_id，如果查询不到user_id则返回0
        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer = user_object

        # 白名单：没有登录都可以访问的url
        # 1.获取当前用户访问的url
        # 2.检查url是否在白名单中，如果在则继续访问，如果不在则判断是否登录成功

        # print(request.path_info)
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return

        # 检查用户是否登录，已登录继续往后走，未登录返回登录页面
        if not request.tracer:
            return redirect('login')
