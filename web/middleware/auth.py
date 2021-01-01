# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2020/12/8 23:05
from django.utils.deprecation import MiddlewareMixin
from web import models


# 中间件
class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """  如果用户已登录，则request中赋值 """
        # 获取user_id，如果查询不到user_id则返回0
        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer = user_object
