# -*- coding:utf-8 -*-

__author__ = 'positever'
__date__ = '2019/10/2 0002 14:29'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequiredMixin,self).dispatch(request,*args,**kwargs)