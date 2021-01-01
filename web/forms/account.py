# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2020/12/4 15:53


from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import random
from utils.tencent.sms import send_sms_single
from django.conf import settings
from utils import encrypt
from django_redis import get_redis_connection
from web.forms.bootstrap import BootStrapForm

import redis


# ModelForm生成注册字段 & 各个字段校验
class RegisterModelForm(BootStrapForm, forms.ModelForm):
    """ ModelForm生成注册字段 & 各个字段校验 """

    # 重写密码格式
    password = forms.CharField(label='密码',
                               min_length=8,
                               max_length=18,
                               error_messages={
                                   'min_length': "密码长度不能小于8个字符",
                                   'max_length': "密码长度不能大于18个字符"
                               },
                               widget=forms.PasswordInput())
    # 添加重复输入密码字段
    confirm_password = forms.CharField(label='重复密码',
                                       min_length=8,
                                       max_length=18,
                                       error_messages={
                                           'min_length': "重复密码长度不能小于8个字符",
                                           'max_length': "重复密码长度不能大于18个字符"
                                       },
                                       widget=forms.PasswordInput())

    # 重写手机号格式，设置正则表达式
    mobile_phone = forms.CharField(label='手机号',
                                   validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ],
                                   widget=forms.TextInput(), )

    # 添加验证码字段
    code = forms.CharField(label='验证码',
                           widget=forms.TextInput())

    class Meta:
        model = models.UserInfo
        # fields = "__all__" 字段默认顺序展示
        # 指定顺序展示
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone', 'code']

    # def __init__(self, *args, **kwargs):
    #     """  重写 __init__方法，统计添加样式 """
    #     super().__init__(*args, **kwargs)
    #     # name:字段名
    #     for name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'  # 统一设置样式
    #         field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)

    def clean_username(self):
        """ 校验用户名 """
        username = self.cleaned_data['username']
        exists = models.UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')
        return username

    def clean_email(self):
        """ 校验邮箱 """
        email = self.cleaned_data['email']
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return email

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 加密并返回
        return encrypt.md5(pwd)

    def clean_confirm_password(self):
        """ 校验重复密码 """
        # pwd = self.cleaned_data['password']
        pwd = self.cleaned_data.get('password')
        confirm_pwd = encrypt.md5(self.cleaned_data['confirm_password'])
        if pwd != confirm_pwd:
            raise ValidationError('两次密码不一致')
        return confirm_pwd

    def clean_mobile_phone(self):
        """ 校验手机号 """
        mobile_phone = self.cleaned_data['mobile_phone']

        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已注册')
            # self.add_error('mobile_phone', '手机号已注册')
        return mobile_phone

    def clean_code(self):
        """ 校验验证码 """
        code = self.cleaned_data['code']
        # mobile_phone = self.cleaned_data['mobile_phone']

        mobile_phone = self.cleaned_data.get('mobile_phone')
        if not mobile_phone:
            return code

        # django-redis
        # conn = get_redis_connection("default")

        # 创建redis连接池
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, encoding='utf-8', max_connections=1000)

        # 去连接池中获取一个连接
        conn = redis.Redis(connection_pool=pool)
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')

        redis_str_code = redis_code.decode('utf-8')
        # strip()去除空格
        if code.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新输入')


# 发送短信验证码 & 校验
class SendSmsForm(forms.Form):
    """  发送短信验证码 & 校验 """

    mobile_phone = forms.CharField(label='手机号',
                                   validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

    # 重写__init__方法，引入request
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    # 点击发送短信，手机号校验的钩子
    def clean_mobile_phone(self):
        """  点击发送短信，手机号校验的钩子 """
        mobile_phone = self.cleaned_data['mobile_phone']

        # 判断短信模板是否有问题
        tpl = self.request.GET.get('tpl')
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            # self.add_error('mobile_phone','短信模板错误')
            raise ValidationError('短信模板错误')

        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if tpl == 'login':
            if not exists:
                raise ValidationError('手机号未注册,请先注册')
        else:
            # 校验数据库是否已有手机号
            if exists:
                raise ValidationError('手机号已存在')

        # 发短信 & 写redis
        # 生成随机验证码
        code = random.randrange(1000, 9999)

        # 发送短信
        sms = result = send_sms_single(mobile_phone, template_id, [code, ])
        if sms['result'] != 0:
            raise ValidationError('短信发送失败,{}'.format(sms['errmsg']))

        # 验证码写入redis
        # 方法一：直接连接redis
        # conn = redis.Redis(host='127.0.0.1', port=6379, encoding='utf-8')

        # 方法二：创建redis连接池
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, encoding='utf-8', max_connections=1000)
        # 去连接池中获取一个连接
        conn = redis.Redis(connection_pool=pool)

        # 方法三：django-redis
        # conn = get_redis_connection()

        conn.set(mobile_phone, code, ex=60)

        return mobile_phone


# 添加短信登录字段 & 各个字段的校验
class LoginSMSForm(BootStrapForm, forms.Form):
    """  添加手机号字段 """
    mobile_phone = forms.CharField(label='手机号',
                                   validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ],
                                   widget=forms.TextInput(), )

    # 添加验证码字段
    code = forms.CharField(label='验证码',
                           widget=forms.TextInput())

    # 校验手机号
    def clean_mobile_phone(self):
        """ 校验手机号 """
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        # user_object = models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        if not exists:
            raise ValidationError('手机号未注册,请先注册')

        return mobile_phone

    # 校验验证码
    def clean_code(self):
        """校验验证码"""
        code = self.cleaned_data['code']
        mobile_phone = self.cleaned_data.get('mobile_phone')

        # 手机号不存在，则验证码无需再校验
        if not mobile_phone:
            return code

        # 创建redis连接池
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, encoding='utf-8', max_connections=1000)
        # 去连接池中获取一个连接
        conn = redis.Redis(connection_pool=pool)
        # 根据手机号去获取验证码
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')

        redis_str_code = redis_code.decode('utf-8')

        if code.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新输入')

        return code


# 添加用户名密码登录字段 & 字段校验
class LoginForm(BootStrapForm, forms.Form):
    username = forms.CharField(label='邮箱或手机号')
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(render_value=True),
                               min_length=8,
                               max_length=18,
                               error_messages={
                                   'min_length': "密码长度不能小于8个字符",
                                   'max_length': "密码长度不能大于18个字符"
                               }, )
    code = forms.CharField(label='图片验证码')

    # 重写__init__方法，引入request
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    # 密码钩子函数 加密并返回
    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 加密并返回
        return encrypt.md5(pwd)

    # 钩子函数 校验图片验证码是否正确
    def clean_code(self):
        """  钩子函数 校验图片验证码是否正确 """
        # 读取用户输入的验证码
        code = self.cleaned_data['code']

        # 获取session中的验证码
        session_code = self.request.session.get('image_code')
        if not session_code:
            raise ValidationError('验证码已过期，请重新获取')

        # 去除空格，不区分大小写
        if code.strip().upper() != session_code.upper():
            raise ValidationError('验证码输入错误')

        return code
