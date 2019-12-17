# -*- coding:utf-8 -*-

__author__ = 'positever'
__date__ = '2019/9/23 0023 8:21'

import xadmin

from .models import UserAsk ,UserCourse,UserMessage,CourseComments,UserFavorite

class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name','add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name','add_time']
    model_icon = 'fa fa-phone'

class UserCourseAdmin(object):
    list_display = ['user', 'course','add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course','add_time']
    model_icon = 'fa fa-book'

class UserMessageAdmin(object):
    list_display = ['user', 'message','has_read','add_time']
    search_fields = ['user', 'message','has_read']
    list_filter = ['user', 'message','has_read','add_time']
    model_icon = 'fa fa-info-circle'

class CourseCommentsAdmin(object):
    list_display = ['user', 'course','comments','add_time']
    search_fields = ['user', 'course','has_read']
    list_filter = ['user', 'course','comments','add_time']
    model_icon = 'fa fa-commenting'

class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id','fav_type','add_time']
    search_fields = ['user', 'fav_id','fav_type']
    list_filter = ['user', 'fav_id','fav_type','add_time']
    model_icon = 'fa fa-envelope'

xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
