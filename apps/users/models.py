# -*- coding:utf-8 -*-
# 自带库
from __future__ import unicode_literals
from datetime import datetime

# 第三方库
from django.db import models
from django.contrib.auth.models import AbstractUser

# 自定义库

# Create your models here.

#继承django默认的auth_user


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name=u"昵称",default="")
    birday = models.DateField(verbose_name=u"生日",null=True,blank=True)
    gender = models.CharField(max_length=6,choices=(("male",u"男"),("female",u"女")),default="女")
    address = models.CharField(max_length=100,default=u"")
    mobile = models.CharField(max_length=11,null=True,blank=True)
    image = models.ImageField(upload_to="image/%Y/%m",default=u"image/default.png",max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def unread_nums(self):
        # 获取用户未读消息的数量
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()

# 邮箱验证码
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length = 20,verbose_name=u"验证码 ")
    email = models.EmailField(max_length=50,verbose_name=u"邮箱")
    # 注册或找回密码均使用，用send_type加以区别
    send_type = models.CharField(verbose_name=u"验证码类型",choices=(("register",u"注册"),("forget",u"找回密码"),("update_email",u"修改邮箱")),max_length=20)
    send_time = models.DateTimeField(verbose_name=u"发送时间",default=datetime.now)  #now不能加括号以生成class实例化的时间，而不是modle编译的时间

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    # 在未加入以下函数时，增加一条数据会显示“修改 EmailVerifyRecord object“
    # 有了以下函数，则显示如'修改admin(xxx@qq.com)'的字样
    def __str__(self):
        # return '%s(%s)'%(self.code,self.email)
        return '{0}({1})'.format(self.code,self.email)

# 轮播图
class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name = u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m",verbose_name=u"轮播图",max_length=100) #存储图片的路径地址
    url = models.URLField(max_length=200,verbose_name=u"访问地址")
    index = models.IntegerField(default=100,verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name