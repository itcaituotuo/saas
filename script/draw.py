# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2020/12/8 13:04

from PIL import Image, ImageDraw

# 创建图片
img = Image.new(mode='RGB', size=(120, 30), color=(253, 245, 230))

draw = ImageDraw.Draw(img, mode='RGB')
# 第一个参数：表示起始坐标
# 第二个参数：表示写入内容
# 第三个参数：表示颜色
draw.text([0, 0], 'python', "red")
# 在图片查看器中打开
# img.show()

# 保存在本地
with open('code.png', 'wb') as f:
    img.save(f, format='png')
