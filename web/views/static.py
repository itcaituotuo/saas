# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2021/3/4 17:36

from django.shortcuts import render


def price(request):
    """  价格策略 """

    return render(request, "static_html/price.html")
