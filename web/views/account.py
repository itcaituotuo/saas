# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2020/12/4 13:44

# 用户账户相关的功能：注册、短信、登录、注销

from django.shortcuts import render, HttpResponse, redirect
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm, LoginForm
from django.http import JsonResponse
from web import models
from django.conf import settings


# 注册
def register(request):
    """ 注册 """
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 验证通过，写入数据库（密码要使用密文存储）
        # data = form.cleaned_data
        # data.pop('code')
        # data.pop('confirm_password')
        # instance = models.UserInfo.objects.create(**data)

        # save()方法只会将ModelForm中定义的字段存入数据库，自动去除code和confirm_password
        # 用户表中新建一条数据（注册）
        form.save()
        return JsonResponse({'status': True, 'data': '/login/'})

    return JsonResponse({'status': False, 'error': form.errors})


# 发送短信验证码
def send_sms(request):
    """ 发送短信验证码 """
    form = SendSmsForm(request, data=request.GET)
    # 只是校验手机号：不能为空、格式是否正确
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


# 短信验证码登录
def login_sms(request):
    """ 短信验证码登录 """
    if request.method == 'GET':
        form = LoginSMSForm()
        return render(request, 'login_sms.html', {'form': form})
    form = LoginSMSForm(request.POST)
    if form.is_valid():
        # 用户输入正确，登录成功
        mobile_phone = form.cleaned_data['mobile_phone']

        # 把用户名写入到session中
        # 拿到用户对象
        user_object = models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        # 信息写入session中
        request.session['user_id'] = user_object.id
        request.session.set_expiry(60 * 60 * 24 * 14)

        # 验证通过，返回True，跳转到index页面
        return JsonResponse({"status": True, 'data': "/index/"})
    return JsonResponse({"status": False, 'error': form.errors})


# 用户名和密码登录
def login(request):
    """  用户名和密码登录 """
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})

    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # user_object = models.UserInfo.objects.filter(username=username, password=password).first()
        # （ 手机=手机 and pwd = pwd ）or （邮箱 = 邮箱 and pwd = pwd）
        from django.db.models import Q
        user_object = models.UserInfo.objects.filter(Q(email=username) | Q(mobile_phone=username)).filter(
            password=password).first()

        if user_object:
            # 用户名密码正确
            request.session['user_id'] = user_object.id
            # 用户信息保留两周时间
            request.session.set_expiry(60 * 60 * 24 * 14)

            return redirect('index')
        form.add_error('username', '用户名或密码错误')

    return render(request, 'login.html', {'form': form})


# 生成图片验证码
def image_code(request):
    """  生成图片验证码 """
    from io import BytesIO
    from utils.image_code import check_code

    image_object, code = check_code()

    # 将图片验证码写入session中
    request.session['image_code'] = code
    # 设置过期时间为60s
    request.session.set_expiry(60)

    # 将图片的内容存储到内存中
    stream = BytesIO()
    image_object.save(stream, 'png')
    # 读取图片二进制内容
    return HttpResponse(stream.getvalue())

    # # 将图片存储到本地
    # with open('code.png', 'wb') as f:
    #     image_object.save(f, format='png')
    #
    # # 本地打开文件（可能会造成多个人获取验证码，但是图片名字一样）
    # with open('code.png', 'rb') as f:
    #     data = f.read()

    return HttpResponse(data)


# 退出
def logout(request):
    """  退出 """
    # 将session中的值清空
    request.session.flush()
    return redirect('index')
