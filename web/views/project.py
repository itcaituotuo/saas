# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2021/3/1 22:07

# render方法可接收三个参数，一是request参数，二是待渲染的html模板文件，三是保存具体数据的字典参数。
# 它的作用就是将数据填充进模板文件，最后把结果返回给浏览器。
from django.shortcuts import render


def project_list(request):
    """  项目列表 """

    return render(request, 'project_list.html')
