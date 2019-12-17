# -*- coding:utf-8 -*-

__author__ = 'positever'
__date__ = '2019/9/22 0022 21:35'

import xadmin

from .models import Course,Lesson,Video,CourseResource,BannerCourse
from organization.models import CourseOrg

class LessonInline(object):
    model = Lesson
    extra = 0

class CourseResourceInline(object):
    model = CourseResource
    extra = 0

class CourseAdmin(object):
    list_display = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time','get_lesson_nums','go_to']
    search_fields = ['name','desc','detail','degree','students','fav_nums','image','click_nums']
    list_filter = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']
    model_icon = 'fa fa-book'
    ordering = ['-click_nums']
    readonly_fields = ['fav_nums','students']
    list_editable = ['degree','desc']
    exclude = ['click_nums']
    inlines = [LessonInline, CourseResourceInline]
    refresh_times = [3,5]  #表示3或5秒刷新一次，在页面中会多一个双追尾箭头图标
    style_fields = {"detail":"ueditor"}
    import_excel = True

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner = False)
        return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES: # 在if语句打上断点，导入xls文件调试
            pass  # 此处是一系列的操作接口, 通过  request.FILES 拿到数据随意操作
        return super(CourseAdmin, self).post(request, args, kwargs)  # 此返回值必须是这样,以防止CourseAdmin保存失败, 否则会报NoneType object has no attribute 'has_header的错


class BannerCourseAdmin(object):
    list_display = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']
    search_fields = ['name','desc','detail','degree','students','fav_nums','image','click_nums']
    list_filter = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']
    model_icon = 'fa fa-book'
    ordering = ['-click_nums']
    readonly_fields = ['fav_nums','students']
    exclude = ['click_nums']
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner = True)
        return qs



class LessonAdmin(object):
    list_display =  ['course','name','add_time']
    search_fields = ['course','name']
    list_filter = ['course__name','name','add_time']
    model_icon = "fa fa-bars"

class VideoAdmin(object):
    list_display =  ['lesson','name','add_time']
    search_fields = ['lesson','name']
    list_filter = ['lesson','name','add_time']
    model_icon = "fa fa-film"

class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download','add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download','add_time']
    model_icon = 'fa fa-file'

xadmin.site.register(CourseResource,CourseResourceAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)