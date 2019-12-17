# -*- coding:utf-8 -*-

__author__ = 'positever'
__date__ = '2019/9/23 0023 17:31'

from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(required = True) #字段不能为空
    password = forms.CharField(required = True,min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)  #对前端传递过来的email进行验证
    password = forms.CharField(required = True,min_length=5)
    captcha = CaptchaField(error_messages={"invalid":r"验证码错误！"})

class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)  #对前端传递过来的email进行验证
    captcha = CaptchaField(error_messages={"invalid":r"验证码错误！"})

class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required = True,min_length=5)
    password2 = forms.CharField(required = True,min_length=5)

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','gender','birday','address','mobile']
