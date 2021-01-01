# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2020/12/8 22:04

from django.shortcuts import render, HttpResponse


def index(request):
    return render(request, 'index.html')
