from django.shortcuts import render, HttpResponse
import random
from utils.tencent.sms import send_sms_single
from django.conf import settings


def send_sms(request):
    """ 发送短信
        ?tpl=login -> 792844
        ?tpl=register -> 792842
    """
    tpl = request.GET.get('tpl')
    template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
    if not template_id:
        return HttpResponse('模板不存在')

    code = random.randrange(1000, 9999)
    res = send_sms_single('1505922449', template_id, [code, ])
    print(res)
    print(code)
    if res['result'] == 0:
        return HttpResponse('成功')
    else:
        return HttpResponse(res['errmsg'])


from django import forms
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


# ModelForm生成注册字段
class RegisterModelForm(forms.ModelForm):
    # 重写手机号格式，设置正则表达式
    mobile_phone = forms.CharField(label='手机号',
                                   validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ],
                                   widget=forms.TextInput(), )
    # 重写密码格式
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput())
    # 重复输入密码
    confirm_password = forms.CharField(label='重复密码',
                                       widget=forms.PasswordInput())
    # 验证码
    code = forms.CharField(label='验证码',
                           widget=forms.TextInput())

    class Meta:
        model = models.UserInfo
        # fields = "__all__" 字段默认顺序展示
        # 指定顺序展示
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # name:字段名
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)


def register(request):
    form = RegisterModelForm()
    return render(request, 'app01/register.html', {'form': form})
