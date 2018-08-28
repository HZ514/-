from django.db import models

# Create your models here.


# 用户表
class User(models.Model):
    u_name = models.CharField(max_length=30,null=False,unique=True)  # 昵称
    u_password = models.CharField(max_length=200,null=False)  # 密码
    u_email = models.CharField(max_length=20,unique=True)  # 邮箱
    u_icon = models.ImageField(upload_to='icons')  # 头像
    is_superuser = models.BooleanField(default=0)  # 是否是超级管理员
    is_delete = models.BooleanField(default=0)  # 是否删2除
    username = models.CharField(max_length=20,null=True)  # 用户真实姓名
    userphone = models.CharField(max_length=11,null=True)  # 用户联系电话
    useraddress = models.CharField(max_length=100,null=True)  # 用户联系地址
    class Meta:
        db_table = 'tt_user'


# 用户收货信息表
class UserReceivInfo(models.Model):
    name = models.CharField(max_length=100)  # 姓名
    phone = models.CharField(max_length=11)  # 联系电话
    relation_address = models.CharField(max_length=200)  # 联系地址
    detail_address = models.CharField(max_length=200)  # 详细地址地址
    postcode = models.CharField(max_length=10)  # 邮编
    is_default = models.BooleanField(default=0)  # 是否是默认地址
    user = models.ForeignKey(User)  # 关联用户

    class Meta:
        db_table = 'tt_userinfo'


# 用户状态表
class UserStatus(models.Model):
    user = models.ForeignKey(User) # 关联用户
    ticket = models.CharField(max_length=255)  # 验证码
    out_time = models.DateTimeField()  # 存活时间

    class Meta:
        db_table = 'user_status'

