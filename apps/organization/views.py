# _*_ encoding:utf-8 _*_
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponse

from .models import CourseOrg,CityDict,Teacher
from .forms import UserAskForm

from operation.models import UserFavorite
from courses.models import Course
# Create your views here.

flag = True

class OrgView(View):
    """
        课程机构列表功能
    """
    def get(self,request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        # 热门机构
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 城市
        all_citys = CityDict.objects.all()

        # 课程搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords)
                    )  # 相当于SQL语句中的like

        # 从url地址取出city的id值到数据库中进行筛选城市
        city_id = request.GET.get('city',"")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct',"")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 按学习人数或课程数进行排列
        sort = request.GET.get('sort',"")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")  #根据学习人数倒序排列
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")  #根据课程数倒序排列

        # 机构数量统计
        org_nums = all_orgs.count()

        # pure-pagination对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1


        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs,5, request=request)   # 其中per_page表示每页显示的个数

        orgs = p.page(page)

        return render(request,'org-list.html',{
            "all_orgs":orgs,
            "all_citys":all_citys,
            "org_nums":org_nums,
            "city_id":city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort
        })

class AddUserAskView(View):
    """
    用户添加咨询
    """

    def post(self,request):
        global flag
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # 此处因不知名的原因会导致user_ask实例化两次，因此使用flag进行标记
            if not flag:
                flag = True
                return
            flag = False

            user_ask = userask_form.save(commit=True)
            # 用户咨询提交是ajax异步操作，需要返回json格式的字符串
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            # return HttpResponse("{'status':'fail','msg':{0}}".format(userask_form.errors),content_type='application/json')
            return HttpResponse('{"status":"fail","msg":"添加出错"}',content_type='application/json')

class OrgHomeView(View):
    """
        机构首页
    """
    def get(self,request,org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        # 前端确定收藏与否的后端标记
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })

class OrgCourseView(View):
    """
        机构课程列表页
    """
    def get(self,request,org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        # 前端确定收藏与否的后端标记
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page': current_page,
            'has_fav':has_fav
        })


class OrgDescView(View):
    """
        机构介绍页
    """
    def get(self,request,org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 前端确定收藏与否的后端标记
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-desc.html',{
            'course_org':course_org,
            'current_page': current_page,
            'has_fav':has_fav
        })


class OrgTeacherView(View):
    """
            机构教师页
        """

    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        # 前端显示收藏与否的后端标记
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
        })



class AddFavView(View):
    """
        用户收藏，用户取消收藏
    """
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)

        # 判断用户是否登录：
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在，则表示用户取消收藏
            exist_records.delete()

            if int(fav_type) == 1:
                course = Course.objects.get(id = int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums =0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id = int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums =0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id = int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums =0
                teacher.save()

            return HttpResponse('{"status":"success","msg":"收藏"}',content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    """
    课程讲师列表页
    """
    def get(self,request):
        all_teachers = Teacher.objects.all()

        # 课程讲师搜索
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords)|Q(work_company__icontains=search_keywords)|Q(work_position__icontains=search_keywords))  # 相当于SQL语句中的like


        # 按人气排序
        sort = request.GET.get('sort',"")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]

        # 机构数量统计
        teacher_nums = all_teachers.count()

        # pure-pagination对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, 1, request=request)  # 其中per_page表示每页显示的个数

        teachers = p.page(page)
        return render(request,"teachers-list.html",{
            "all_teachers":teachers,
            "sorted_teacher":sorted_teacher,
            "sort":sort,
            "teacher_nums":teacher_nums,

        })


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)

        has_teacher_faved = False
        if UserFavorite.objects.filter(user = request.user, fav_type = 3, fav_id = teacher.id):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user = request.user, fav_type = 2, fav_id = teacher.org.id):
            has_org_faved = True


        # 讲师排行
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        return render(request, "teacher-detail.html", {
            "teacher":teacher,
            "all_courses":all_courses,
            "sorted_teacher":sorted_teacher,
            'has_teacher_faved':has_teacher_faved,
            'has_org_faved':has_org_faved
        })

# 金歌一笑玉枕美，
# 罗兰水中蝶梦飞。
# 宝马帘里花想月，
# 多谢秋高诗画谁。