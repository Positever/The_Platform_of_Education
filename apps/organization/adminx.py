# -*- coding:utf-8 -*-

__author__ = 'positever'
__date__ = '2019/9/23 0023 8:06'

import xadmin

from .models import CityDict,CourseOrg,Teacher

class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']
    model_icon = 'fa fa-star'


class CourseOrgaAdmin(object):
    list_display = ['name', 'desc', 'click_nums','fav_nums','image','address','city','add_time']
    search_fields = ['name', 'desc', 'click_nums','fav_nums','image','address','city']
    list_filter = ['name', 'desc', 'click_nums','fav_nums','image','address','city','add_time']
    model_icon = 'fa fa-university'
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years','work_company']
    search_fields = ['org', 'name', 'work_years','work_company']
    list_filter = ['org', 'name', 'work_years','work_company']
    model_icon = 'fa fa-user-circle-o'

xadmin.site.register(Teacher,TeacherAdmin)
xadmin.site.register(CourseOrg,CourseOrgaAdmin)
xadmin.site.register(CityDict,CityDictAdmin)