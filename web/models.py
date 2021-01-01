from django.db import models


# Create your models here.

# 创建用户表
class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32, db_index=True)  # db_index=True创建索引
    email = models.EmailField(verbose_name='邮箱', max_length=32)  # EmailField定义了邮箱的正则表达式
    mobile_phone = models.CharField(verbose_name='手机号', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)


# 价格策略表
class PricePolicy(models.Model):
    """  价格策略表 """
    category_choices = (
        (1, '免费版'),
        (2, '收费版'),
        (3, '其他'),
    )
    category = models.SmallIntegerField(verbose_name='收费类型',
                                        default=2,
                                        choices=category_choices)  # SmallIntegerField 短整数
    title = models.CharField(verbose_name='标题', max_length=32)
    price = models.PositiveIntegerField(verbose_name='价格')  # PositiveIntegerField 表示正整数类型

    project_num = models.PositiveIntegerField(verbose_name='项目数')
    project_member = models.PositiveIntegerField(verbose_name='项目成员数')
    project_space = models.PositiveIntegerField(verbose_name='单项目空间')
    per_file_size = models.PositiveIntegerField(verbose_name='单文件大小(M)')

    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


# 交易记录表
class Transaction(models.Model):
    """ 交易记录 """
    status_choice = (
        (1, '未支付'),
        (2, '已支付')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choice)

    order = models.CharField(verbose_name='订单号', max_length=64, unique=True)  # unique=True 唯一索引

    user = models.ForeignKey(verbose_name='用户', to='UserInfo')
    price_policy = models.ForeignKey(verbose_name='价格策略', to='PricePolicy')

    count = models.IntegerField(verbose_name='数量（年）', help_text='0表示无限期')
    price = models.IntegerField(verbose_name='实际支付价格')

    start_datetime = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    end_datetime = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


# 项目表
class Project(models.Model):
    """ 项目表 """
    # 颜色
    COLOR_CHOICES = (
        (1, "#FFDEAD"),
        (2, "#00E5EE"),
        (3, "#43CD80"),
        (4, "#00BFFF"),
        (5, "#FFD700"),
        (6, "#FF6A6A"),
        (7, "#DA70D6"),
    )

    name = models.CharField(verbose_name='项目名', max_length=32)
    color = models.SmallIntegerField(verbose_name='颜色', choices=COLOR_CHOICES, default=1)
    desc = models.CharField(verbose_name='项目描述', max_length=255, null=True, blank=True)

    use_space = models.BigIntegerField(verbose_name='项目已使用空间', default=0, help_text='字节')

    star = models.BooleanField(verbose_name='星标', default=False)  # BooleanField 布尔值

    join_count = models.SmallIntegerField(verbose_name='参与人数', default=1)
    creator = models.ForeignKey(verbose_name='创建者', to='UserInfo')
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    # 查询：可以省事
    # 增加、删除、修改无法完成
    # project_user = models.ManyToManyField(to='UserInfo', through='ProjectUser', through_fields=('project', 'user'))


# 项目参与者表
class ProjectUser(models.Model):
    """ 项目参与者 """
    project = models.ForeignKey(verbose_name='项目', to='Project')
    user = models.ForeignKey(verbose_name='参与者', to='UserInfo')
    star = models.BooleanField(verbose_name='星标', default=False)

    # invitee = models.ForeignKey(verbose_name='邀请者', to='UserInfo', related_name='b')

    create_datetime = models.DateTimeField(verbose_name='加入时间', auto_now_add=True)

# # 反向关联
# obj = UserInfo.objects.filter(id=1)
# # obj.projectuser_set.all()
# obj.a.all()
