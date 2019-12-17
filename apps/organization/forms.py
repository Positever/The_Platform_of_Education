# -*- coding:utf-8 -*-

__author__ = 'positever'
__date__ = '2019/9/27 0027 8:23'

import re
from django import forms

from operation.models import UserAsk


# modelform代码如下(验证成功后可以调用save方法保存到数据库）
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk  # 选择需要继承的用户咨询类UserAsk
        fields = ['name','mobile','course_name']  # 选择需要继承的字段

    # 验证mobile,此函数必须以clean开头
    def clean_mobile(self):
        """
            验证手机号码是否合法
        """
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法",code="mobile_invalid")