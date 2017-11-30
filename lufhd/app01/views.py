from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import JsonResponse,HttpResponse
from rest_framework import serializers
from rest_framework import viewsets



from . import models
from app01.utils.commons import gen_token
from app01.utils.auth import LuffyAuthentication


# Create your views here.


# class CourseSerialize(serializers.ModelSerializer):
#     level = serializers.CharField(source="get_level_display")
#     class Meta:
#         model = models.Course
#         fields = ['id',"name","course_img","brief","level","pub_date",'period','order']
#
# class courseView(APIView):
#     """
#     学位课列表
#     """
#     # authentication_classes = [LuffyAuthentication,]
#
#     def get(self,request,*args,**kwargs):
#         course_list = models.Course.objects.all()
#         ser = CourseSerialize(instance=course_list, many=True, context={'request': request})
#         return Response(ser.data)
#
# class teachersField(serializers.CharField):
#     def get_attribute(self, instance):
#         teacher_list = instance.teachers.all()
#         return teacher_list
#     def to_representation(self, value):
#         ret = []
#         for row in value:
#             ret.append({'id':row.id,'name':row.name,'title':row.title,'brief':row.brief})
#         return ret
#
# class coursesField(serializers.CharField):
#     def get_attribute(self, instance):
#         courses_list = instance.recommend_courses.all()
#         return courses_list
#     def to_representation(self, value):
#         ret = []
#         for row in value:
#             ret.append({'id':row.id,'name':row.name})
#         return ret

#---------------------------------
# class pricePolicyField(serializers.CharField):
#     def get_attribute(self, instance):
#         courses_list = pricePolicy
#         return courses_list
#     def to_representation(self, value):
#         ret = []
#         for row in value:
#             ret.append({'id':row.valid_period,'name':row.price})
#         return ret



# class courseDetailSerialize(serializers.ModelSerializer):
#     # course = serializers.HyperlinkedIdentityField(view_name="coursedetail-detail")
#     course = serializers.CharField(source="course.name")
#     # teachers = serializers.CharField(source="teachers.all")
#     teachers = teachersField()
#     recommend_courses = coursesField()
#     class Meta:
#         model = models.CourseDetail
#         fields = "__all__"
#         # fields = ['id',"course","why_study","what_to_study_brief","career_improvement","prerequisite"]
#
#
# class courseDetailView(APIView):
#     """
#     课程详细
#     """
#     # authentication_classes = [LuffyAuthentication,]
#     def get(self,request,*args,**kwargs):
#         pk = kwargs.get('pk')
#         print(pk)
#         course_data = models.CourseDetail.objects.get(id=pk)
#         pricePolicy = course_data.course.price_policy.all()
#         print(pricePolicy)
#
#         ser = courseDetailSerialize(instance=course_data, many=False, context={'request': request})
#         return Response(ser.data)
#
# class pricePolicySerialize(serializers.ModelSerializer):
#     valid_period = serializers.CharField(source="get_valid_period_display")
#     class Meta:
#         model = models.PricePolicy
#         # fields = "__all__"
#         fields = ['valid_period',"price",]
#
#
# class pricePolicyView(APIView):
#     """
#     价格策略
#     """
#
#     def get(self,request,*args,**kwargs):
#         pk = kwargs.get('pk')
#         print(pk)
#         course_data = models.CourseDetail.objects.get(id=pk)
#         pricePolicy = course_data.course.price_policy.all()
#         ser = pricePolicySerialize(instance=pricePolicy, many=True, context={'request': request})
#         return Response(ser.data)


#-------------------------------------------
# class MyField(serializers.CharField):
#
#     def get_attribute(self, instance):
#         teacher_list = instance.teachers.all()
#         return teacher_list
#
#     def to_representation(self, value):
#         ret = []
#         for row in value:
#             ret.append({'id': row.id,'name':row.name})
#         return ret


class loginView(APIView):

    def post(self, request, *args, **kwargs):
        """
        用户登录功能，获取用户提交的用户名和密码，如果用户名和密码正确，则生成Token,并返回给用户
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ret = {'code': 1000, 'msg': None}
        user = request.data.get('username')
        pwd = request.data.get('password')
        print(user,pwd)
        user_obj = models.Account.objects.filter(username=user, password=pwd).first()
        if user_obj:
            tk = gen_token(user)
            models.Token.objects.update_or_create(user=user_obj, defaults={'token': tk})
            ret['code'] = 1001
            ret['username'] = user
            ret['token'] = tk
        else:
            ret['msg'] = "用户名或密码错误"
        return JsonResponse(ret)

class CouserSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='get_level_display')
    class Meta:
        model = models.Course
        fields = ['id','name',"brief",'course_img','level_name']


class courseDetailSerialize(serializers.ModelSerializer):

    # valid_period = serializers.CharField(source="get_valid_period_display")
    course = serializers.CharField(source="course.name")
    recommend_courses_list = serializers.SerializerMethodField()
    price_policy_list = serializers.SerializerMethodField()
    teachers_list = serializers.SerializerMethodField()
    class Meta:
        model = models.CourseDetail
        fields = "__all__"


    def get_teachers_list(self,obj):
        ret = []
        course_list = obj.teachers.all()
        for item in course_list:
            ret.append({'id':item.id,'name':item.name,'title':item.title,'brief':item.brief})
        return ret


    def get_recommend_courses_list(self,obj):
        ret = []
        course_list = obj.recommend_courses.all()
        for item in course_list:
            ret.append({'id':item.id,'name':item.name})
        return ret

    def get_price_policy_list(self, obj):
        # 当前课程所有的价格策略
        # valid_period = serializers.CharField(source="get_valid_period_display")
        ret = []
        price_policy_list = obj.course.price_policy.all()
        for item in price_policy_list:
            ret.append({'id':item.id,'price':item.price,"validPeriod":item.get_valid_period_display()})
        return ret

        # return ret

        # ret = []
        # price_policy_list = models.PricePolicy.objects.filter(content_type__app_label='repository',
        #                                   content_type__model='course',
        #                                   object_id=obj.couser_id)
        # return ret

# class CouserDetailSerializer(serializers.ModelSerializer):
#     course_name = serializers.CharField(source='course.name')
#     recommend_courses_list = serializers.SerializerMethodField()
#     price_policy_list = serializers.SerializerMethodField()
#
#     class Meta:
#         model = models.CourseDetail
#         fields = ['id','id',"course","why_study","what_to_study_brief","career_improvement","prerequisite",'course_name','recommend_courses_list']
#
#     def get_recommend_courses_list(self,obj):
#         ret = []
#         course_list = obj.recommend_courses.all()
#         for item in course_list:
#             ret.append({'id':item.id,'name':item.name})
#         return ret
#
#     def get_price_policy_list(self,obj):
#         # 当前课程所有的价格策略
#         # ret = []
#         # price_policy_list = obj.course.price_policy.all()
#         # return ret
#
#         # ret = []
#         # price_policy_list = models.PricePolicy.objects.filter(content_type__app_label='repository',
#         #                                   content_type__model='course',
#         #                                   object_id=obj.couser_id)
#         # return ret
#         return "ssss"
#
#
#
#     def get_price_policy_list(self,obj):
#         # 当前课程所有的价格策略
#         # ret = []
#         # price_policy_list = obj.course.price_policy.all()
#         # return ret
#
#         # ret = []
#         # price_policy_list = models.PricePolicy.objects.filter(content_type__app_label='repository',
#         #                                   content_type__model='course',
#         #                                   object_id=obj.couser_id)
#         # return ret
#         return "ssss"


class CouserView(APIView):

    def get(self,request,*args,**kwargs):
        from django.core.exceptions import ObjectDoesNotExist
        response = {'code': 1000, 'msg': None, 'data': None}
        try:
            pk = kwargs.get('pk')
            if pk:
                # 详细
                detail = models.CourseDetail.objects.get(course_id=pk)
                ser = courseDetailSerialize(instance=detail,many=False)
            else:
                queryset = models.Course.objects.exclude(course_type=2)
                ser = CouserSerializer(instance=queryset, many=True)
            response['data'] = ser.data
        except ObjectDoesNotExist as e:
            response['code'] = 1001
            response['msg'] = '查询课程不存在'
        except IndexError as e:
            pass
        except Exception as e:
            # 错误信息写入日志
            response['msg'] = '查询课程失败'
            response['code'] = 1001

        return Response(response)

























