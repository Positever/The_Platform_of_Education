# _*_ coding:utf-8 _*_
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.views.generic import TemplateView  #用于处理静态文件
import xadmin
from django.views.static import serve

# from users.views import user_login
from users.views import LoginView, LogoutView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView
from users.views import IndexView, LoginUnsafeView
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$',IndexView.as_view(),name="index"),
    # url('^login/$',TemplateView.as_view(template_name="login.html"),name="login")
    # url('^login/$',user_login,name="login")
    url('^login/$',LoginView.as_view(),name="login"),
    # url('^login/$',LoginUnsafeView.as_view(),name="login"),
    url('^logout/$', LogoutView.as_view(), name="logout"),
    url('^register/$',RegisterView.as_view(),name="register"),
    url(r'^captcha/',include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name="user_active"),   #?P提取变量Parameters的意思,正则表达式.*会把active后面的字符全部取出并给到尖括号里
    url(r'^forget/$',ForgetPwdView.as_view(),name="forget_pwd"),
    url(r'^reset/(?P<reset_code>.*)/$',ResetView.as_view(),name="reset_pwd"),   #?P提取变量Parameters的意思,正则表达式.*会把reset后面的字符全部取出并给到尖括号里
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    # 课程机构url配置
    url(r'^org/',include('organization.urls',namespace="org")),  # namespace命名空间可以准确的定位，避免name的重复冲突

    # 课程相关url配置
    url(r'^course/', include('courses.urls', namespace="course")),  # namespace命名空间可以准确的定位，避免name的重复冲突

    # # 教师相关url配置
    # url(r'^teacher/', include('organization.urls', namespace="teacher")),  # namespace命名空间可以准确的定位，避免name的重复冲突

    #  配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)/$',serve,{"document_root":MEDIA_ROOT}),

    # url(r'^static/(?P<path>.*)/$',serve,{"document_root":STATIC_ROOT}),

    # 课程相关url配置
    url(r'^users/', include('users.urls', namespace="users")),  # namespace命名空间可以准确的定位，避免name的重复冲突

    # 富文本相关url
    url(r'^ueditor/', include('DjangoUeditor.urls')),

]

#全局404页面配置
handler404 = 'users.views.page_not_found'
#全局500页面配置
handler500 = 'users.views.page_error'