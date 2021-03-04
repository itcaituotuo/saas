# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2020/12/5 21:52


class BootStrapForm(object):
    def __init__(self, *args, **kwargs):
        """  重写 __init__方法，统一添加样式 """
        super().__init__(*args, **kwargs)
        # name:字段名
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'  # 统一设置样式
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)
