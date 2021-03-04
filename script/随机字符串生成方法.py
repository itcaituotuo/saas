# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2021/3/1 21:34

import uuid

uid = str(uuid.uuid4())  # 根据当前时间和网卡生成一个随机字符串，理论上是不会重复的
print(uid)  # 4762f199-e8c6-4714-8e00-5a5d52a0c514
