#coding:utf-8
#coding:gbk
import hashlib
from math import floor
import pickle
import subprocess
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils import simplejson
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from account.views import handleDynamic
from log.models import Log
from log.views import write_extenal_mail_log
from newchama.helper import send_email_by_mq, send_email_by_mq_multiple
from newchama.settings import EMAIL_HOST_USER
from sales.views import _get_project_link
from services.helper import Helper
from services.models import Member,Company,Demand,ProjectAttach, RecommondItem, ProjectTargetCompanyDetail, AccessToken,EntryForm,MobileValidCode, \
    Favorites, ProjectKeyword, TypeFavorite, ProjectTag, Message, Industry
from api.serializers import *
#from api.serializers import CountrySerializer,ProvinceSerializer,MemberSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
import datetime
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie
import base64
import random,string
#import json
from django.contrib import messages
from django.utils.translation import ugettext, ugettext_lazy as _
import jsonpickle
import logging
import os
import json

logger = logging.getLogger(__name__)
now = datetime.datetime.now()
default_page_size = 10
max_access_time = 30*60    #30min
person_email=['163.com','126.com','qq.com','sina.com','sohu.com','me.com','hotmail.com',
              'yahoo.com.cn','tom.com','hexun.com','21cn.com','sohu.com','sogou.com',
              '56.com','3126.com','mail.china.com','china.com','gmail.com','139.com',
              '5ydns.com','263.com','yahoo.fr']

def handle_page(request):
    curr_page = int(request.GET.get("page", 0))
    page_size = int(request.GET.get("pageSize", 0))
    if curr_page == 0:
        curr_page = 1
    if page_size == 0:
        page_size = default_page_size
    start_record = (curr_page - 1) * page_size
    end_record = curr_page * page_size
    return start_record, end_record

def get_access_token(id):
    time = str(now.strftime('%Y%m%d%H%M%S'))
    access_token = str(id) + "_" + time
    access_token = base64.encodestring(access_token).replace("\n","")
    return access_token #加密
    #base64.decodestring(access_token) 解密

#检查access_token
def check_access_token(request):
    if True:
        return 1
    if request.method == 'POST':
        request_data = request.DATA
        access_token = request_data["access_token"]
    elif request.method == 'GET':
        access_token = request.GET.get("access_token")
    if access_token:
        expire_time = (now - datetime.timedelta(seconds=30*60))
        at = AccessToken.objects.get(access_token=access_token, login_date__gt=expire_time)
        if at:
            return at.member_id
    return False

#产生随机数
def GenRandomNum(length):
    #随机出数字的个数
    numOfNum = random.randint(length,length)
    #选中numOfNum个数字
    slcNum = [random.choice(string.digits) for i in range(numOfNum)]
    random.shuffle(slcNum)
    #生成随机数
    genRandomNum = ''.join([i for i in slcNum])
    return genRandomNum

#登录
@api_view(['POST'])
def login(request):
    c = {}
   # c["data"] = ""
    c["status"] = "fail"
    c["message"] = "username or password can not be null"
    c["access_token"] = ""
    c["ry_token"] = ""
   # c["de_access_token"] = ""
    request_data = request.DATA
    if len(request_data) > 0:
        login_post_username = request_data["account"]
        login_post_password = request_data["password"]
        m, bool = Member.login(login_post_username, login_post_password)
        cmd = 'curl -X POST -H "App-Key: pwe86ga5elue6" -H "Nonce: 39486779" -H "Timestamp: 1433501301" -H "Signature: 8c6f164d23683bdcb90c34c8b1ef5ca880320ce9" -d "userId='+login_post_username+'"   https://api.cn.rong.io/user/getToken.json'
        handle = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
        if bool and handle:
            AccessToken.objects.filter(member_id=m.id).delete()
           # serializer = LoginSerializer(m)
            access_token = get_access_token(m.id)
            AccessToken.objects.create(member=m, access_token=access_token, login_date=now)
            result = handle.stdout.read()
            res = json.loads(result)
            #c["data"] = serializer.data
            c["status"] = "success"
            c["message"] = "login success"
            c["access_token"] = access_token
            c["ry_token"] = res["token"]
           # c["de_access_token"] = base64.decodestring(access_token)
        else:
            c["message"] = m
    return Response(c)

#第三方登录，待完善
@api_view(['POST'])
def other_way_login(request):
    c = {}
    c["status"] = "fail"
    c["message"] = "username or password can not be null"
    c["access_token"] = ""
    request_data = request.DATA
    if len(request_data) > 0:
        other_way_login_id = request_data["id"]
        other_way_login_type = request_data["type"]
        other_way_login_other_access_token = request_data["other_access_token"]
    return Response(c)

#注册
@api_view(['POST'])
def register(request):
    c = {}
    c["status"] = "fail"
    c["message"] = "Information can not be null"
    c["access_token"] = ""
    is_valid = True
    is_exist = False
    request_data = request.DATA
    '''
     is_cn = request.lang == 'zh-cn'
    mobile_intel = 86
    if is_cn is False:
        mobile_intel = 1
    '''
    if len(request_data) > 0:
        register_post_mobilephone = request_data["mobilephone"]
        register_post_passwd = request_data["password"]
        register_post_valid_code = request_data["valid_code"]
        expire_time = (now - datetime.timedelta(seconds=30*60))
        m = MobileValidCode.objects.get(mobile=register_post_mobilephone, add_time__gt=expire_time)
        if register_post_mobilephone.strip == "":
            is_valid = False
            c["message"] = "mobile can not be null,please input your mobilephone"
        if register_post_passwd.strip() == "":
            is_valid = False
            c["message"] = "password can not be null,please input your password"
        if register_post_valid_code.strip == "":
            is_valid = False
            c["message"] = "valid code can not be null,please input the valid code"
        if MobileValidCode.objects.get(mobile=register_post_mobilephone).valid_code != register_post_valid_code:
            is_valid = False
            c["message"] = "valid code is not correct"
        if not m:
            is_valid = False
            c["message"] = "valid code is time out"


        if is_valid:
            count_mobile = Member.objects.filter(mobile=register_post_mobilephone).count()
            if count_mobile > 0:
                is_exist = True
                c["message"] = "the mobilephone is existed"

            if is_exist is False:
                m1 = Member()
                m1.mobile = register_post_mobilephone
                m1.make_password(register_post_passwd)
                m1.company_id = 1 #company这块需要更改
                m1.save()
                c["message"] = "register success!"
                c["status"] = "success"
                register_set = Member.objects.get(mobile=register_post_mobilephone)
                c["access_token"] = get_access_token(register_set.id)
                at = AccessToken()
                at.member = m1
                at.access_token = c["access_token"]
                at.save()
    return Response(c)


#用户认证
@api_view(['POST'])
def user_identify(request):
    c = {}
    c["status"] = "fail"
    c["message"] = "Information can not be null"
    is_valid = True
    is_exist = False
    request_data = request.DATA

    if len(request_data) > 0:
        user_identify_post_email = request_data["email"]
        user_identify_post_username = request_data["username"]
        user_identify_post_companyname = request_data["companyname"]
        user_identify_post_companytype = request_data["companytype"]
        user_identify_post_job_title = request_data["job_title"]
        user_identify_post_access_token = request_data["access_token"]

        if not check_access_token(request):
            is_valid = False
            c["messages"] = "access token expired or not login"
        if user_identify_post_email.strip() == "":
            is_valid = False
            c["message"] = "email can not be null,please input your email"
        if user_identify_post_username.strip == "":
            is_valid = False
            c["messages"] = "username can not be null,please input your username"
        if user_identify_post_companyname.strip() == "":
            is_valid = False
            c["message"] = "company name can not be null,please input your company"
        if user_identify_post_companytype.strip() == "":
            is_valid = False
            c["message"] = "company type can not be null,please select your company type"
        if user_identify_post_job_title.strip() == "":
            is_valid = False
            c["messages"] = "job title can not be null,please input your job title"


        if is_valid:
            count_email = Member.objects.filter(email=user_identify_post_email).count()
            if count_email>0:
                is_exist=True
                c["message"] = "the email is existed"

            at_id = AccessToken.objects.get(access_token=user_identify_post_access_token).member_id
            m = Member.objects.get(id=at_id)
            m.email = user_identify_post_email
            m.first_name = user_identify_post_username
            cmp = Company()
            cmp.name_cn = user_identify_post_companyname
            cmp.type = user_identify_post_companytype
            m.company = cmp
            m.position_cn = user_identify_post_job_title
            if is_exist is False:
                if len(m.email.split('@'))>1:
                    email_domain=m.email.split('@')[1]
                    if email_domain in person_email:
                        m.save()
                        c["message"] = "commit success!"
                        c["status"] = "success"

                    else:
                        _company_num=Company.objects.filter(name_cn=m.company).count()
                        if _company_num==0:
                            _new_company=Company()
                            _new_company.name_cn=m.company
                            _new_company.type=int(m.company.type)

                            _new_company.data_source='User add'
                            _new_company.save()
                        else:
                            _new_company=get_object_or_404(Company,name_cn=m.company)

                        _new_user=Member()
                        _new_user.company=_new_company
                        _new_user.type=3
                        _new_user.status=4
                        _new_user.first_name=m.fullname
                       # _new_user.mobile_intel=form.mobile_intel
                        _new_user.mobile=Member.objects.get(id=at_id).mobile
                        _new_user.email=m.email
                        _tmp_code = hashlib.new('md5', str(now)+user_identify_post_email).hexdigest()
                        _new_user.activecode=_tmp_code

                        _new_user.make_password(m.password)
                        _new_user.expire_date=now+datetime.timedelta(days=365)
                        _new_user.save()
                        c["message"] = "commit success!"
                        c["status"] = "success"

    return Response(c)

#获取验证码
@api_view(['GET'])
def get_valid_code(request):
    c = {}
    c["status"] = "fail"
    c["message"] = "Information can not be null"
    m=MobileValidCode()
    get_valid_code_get_mobile = request.GET.get("mobile")
    if get_valid_code_get_mobile:
            MobileValidCode.objects.filter(mobile=get_valid_code_get_mobile).delete()
            valid_code = GenRandomNum(6)#产生6位随机数
            m.mobile = get_valid_code_get_mobile#保存到数据库mobilevalidcode
            m.valid_code = valid_code
            m.save()
            content = "您好，你的手机".decode('UTF-8') + get_valid_code_get_mobile + "的验证码为：".decode('UTF-8') + valid_code + "，该验证码在30分钟内有效,请尽快输入".decode('UTF-8')
            ####调用短信接口 sendsms(mobile, content)
            cmd = 'curl -X POST -H \"X-AVOSCloud-Application-Id: af3g1csegc91gm01mckbjokvr4fk3g4mdjex89c8tk3oy0q3\" -H \"X-AVOSCloud-Application-Key: bcm1yqprcu6l07xd2opd670711b79s4u3oomi0uuwpyhsoz1\"   -H \"Content-Type: application/json\"   -d \'{\"mobilePhoneNumber\": \"'+get_valid_code_get_mobile+'\",\"template\":\"message1\",\"valid_code\":\"'+valid_code+'\"}\' https://api.leancloud.cn/1.1/requestSmsCode'
            result = os.system(cmd)
            if result == 0:
                c["status"] = "success"
            c["message"] = content
    return Response(c)

#动态主页获取用户动态列表
@api_view(['GET'])
def get_dynamic_msg_list(request):
    c = {}
    c["data"]=""
    c["message"]="Fail to get dynamic message"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    if mem_id:
        start_record, end_record = handle_page(request)
        timeline = handleDynamic(mem_id,start_record, end_record)
        serializer = Get_Dynamic_Msg_ListSerializer(data=timeline, many=True)
        serializer.is_valid()
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "success get dynamic message"
    return Response(c)

#获得用户详情
@api_view(['GET'])
def get_user_detail(request):
    c = {}
    c["data"]=""
    c["message"]="Fail to get user detail"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    if mem_id:
        get_user_detail_set = Member.objects.get(pk=mem_id)
        c["focus_aspect"] = get_user_detail_set.member_focus_aspect()
        serializer = Get_User_Detail_Serializer(get_user_detail_set)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#关注用户
@api_view(['GET'])
def focus_user(request):
    c = {}
    c["message"]="focus failed"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    member = Member.objects.get(pk=mem_id)
    user_id = request.GET.get("user_id")
    if mem_id:
        reciver = Member.objects.get(pk=user_id)
        member.add_member_to_favorites(reciver)
        c["status"] = "success"
        c["message"] = "focus success"
    return Response(c)

#获得用户发布的项目列表
@api_view(['GET'])
def get_user_publish_pro_list(request):
    c = {}
    c["data"]=""
    c["message"]="Fail to get user publish pro list"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    if mem_id:
        start_record, end_record = handle_page(request)
        get_user_publish_pro_list_set = Project.objects.filter(member_id=mem_id)[start_record : end_record]
        serializer = Get_User_Publish_Pro_List_Serializer(get_user_publish_pro_list_set,many=True)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#获得用户关注的项目列表
@api_view(['GET'])
def get_user_care_pro_list(request):
    c = {}
    c["data"]=""
    c["message"]="Fail to get user care pro list"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    if mem_id:
        start_record, end_record = handle_page(request)
        get_user_care_pro_list_set = Favorites.objects.filter(member_id=mem_id)[start_record : end_record]
        serializer = Get_User_Care_Pro_List_Serializer(get_user_care_pro_list_set, many=True)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)


#获得用户关注的好友列表
@api_view(['GET'])
def get_user_care_mem_list(request):
    c = {}
    c["data"]=""
    c["message"]="Fail to get user care mem list"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    if mem_id:
        start_record, end_record = handle_page(request)
        get_user_care_member_list_set = Favorites.objects.filter(member_id=mem_id,type_relation=TypeFavorite.member)[start_record : end_record]
        serializer = Get_User_Care_Member_List_Serializer(get_user_care_member_list_set, many=True)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)


#获得项目详情
@api_view(['GET'])
def get_pro_detail(request):
    c = {}
    c["pro_data"]=""
    c["message"]="Fail to get pro detail"
    c["status"] = "fail"
    pro_id = request.GET.get("pro_id")
    mem_id = check_access_token(request)
    if mem_id:
        get_pro_detail_set = Project.objects.get(pk=pro_id)
        ss = get_pro_detail_set.project_stock_structure.all()
        if ss:
            s = {}
            s["management"] = str(int(ss[0].rate))
            s["personal"] = str(int(ss[1].rate))
            s["other"] = str(int(ss[2].rate))
        # serializer_pro_stock_structure = Get_Pro_Stock_Structure_Serializer(ss,many=True)
        serializer = Get_Pro_Detail_Serializer(get_pro_detail_set)
        get_pro_detail_tag = ProjectTag.objects.filter(project_id=pro_id)
        serializer_pro_tag = Get_Pro_Detail_Tag_Serializer(get_pro_detail_tag,many=True)
        get_pro_keywords = ProjectKeyword.objects.filter(project_id=pro_id)
        serializer_pro_keywords = Get_Pro_Keywords_Serializer(get_pro_keywords,many=True)
        c["company_tag"] = serializer_pro_tag.data
        c["project_keywords"] = serializer_pro_keywords.data
        c["pro_data"] = serializer.data
        c['curr_year'] = get_pro_detail_set.financial_year
        c['last_year'] = get_pro_detail_set.financial_year - 1
        c['last_year_before'] = get_pro_detail_set.financial_year - 2
        c['stockST'] = s
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#发送消息给用户
@api_view(['GET'])
def send_msg_to_publisher(request):
    c = {}
    c["message"]="Fail to send message"
    c["status"] = "fail"
    sender_id = check_access_token(request)
    receiver_id = request.GET.get("receiver_id")
    content = request.GET.get("content")
    common_id  = request.GET.get("common_id")
    type = request.GET.get("type")
    messages = Message()
    if sender_id:
        if type == '0':
            messages.sender_id = sender_id
            messages.receiver_id = receiver_id
            messages.content = content
            messages.type_relation = type
            messages.save()
        elif type == '1':
            messages.sender_id = sender_id
            messages.receiver_id = receiver_id
            messages.content = content
            messages.project_id = common_id
            messages.type_relation = type
            messages.save()
        elif type == '2':
            messages.sender_id = sender_id
            messages.receiver_id = receiver_id
            messages.content = content
            messages.demand_id = common_id
            messages.type_relation = type
            messages.save()
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#关注项目
@api_view(['GET'])
def focus_pro(request):
    c = {}
    c["message"]="Fail to focus project"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    pro_id = request.GET.get("pro_id")
    member = Member.objects.get(pk=mem_id)
    if mem_id:
        pro = Project.objects.get(pk=pro_id)
        member.add_project_to_favorites(pro)
        c["status"] = "success"
        c["message"] = "focus project success"
    return Response(c)

#标记不合适项目，需要改动较大，后期处理
@api_view(['POST'])
def define_pro_not_proper(request):
    c = {}
    pro_not_interest_pro_id = 1
    pro_not_interest_set = Project.objects.get(id=pro_not_interest_pro_id)
    serializer = Define_Pro_Not_Proper_Serializer(pro_not_interest_set)
    c["data"] = serializer.data
    c["status"] = "success"
    c["message"] = "ok"
    return Response(c)

#分享项目，需要记录到log?
@api_view(['GET'])
def pro_share(request):
    c = {}
    c["message"]="Fail to share project"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    #pro_id = request.GET.get("pro_id")
    share_way = request.GET.get("share_way")
    if mem_id:
        if share_way == 1:
            c["messages"] = "share weixin success"
        elif share_way == 2:
            c["messages"] = "share weibo success"
        c["status"] = "success"
    return Response(c)

#市场主页获得用户发布的项目和需求列表
@api_view(['GET'])
def get_pro_and_demand_list(request):
    c = {}
    c["message"]="Fail to get pro and demand list"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    if mem_id:
        start_record, end_record = handle_page(request)
        pro_list_set = Project.objects.filter().all()[start_record : end_record]
        serializer_pro = Get_Pro_List_Serializer(pro_list_set,many=True)
        demand_list_set = Demand.objects.filter().all()[start_record : end_record]
        serializer_demand = Get_Demand_List_Serializer(demand_list_set,many=True)
       # c["pro_data"] = serializer_pro.data
       # c["demand_data"] = serializer_demand.data
        c["data"] = serializer_pro.data+serializer_demand.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#筛选获取项目列表
@api_view(['GET'])
def get_target_pro_list(request):
    mem_id = check_access_token(request)
    c = {}
    c["message"]="Fail to get pro list"
    c["status"] = "fail"
    #company_tag = request.GET.get("company_tag") 可选
    first_industry = request.GET.get("first_industry")
    second_industry = request.GET.get("second_industry")
    area_country = request.GET.get("area_country")
    area_province = request.GET.get("area_province")
    if mem_id:
        start_record, end_record = handle_page(request)
        get_target_pro_list_set = Project.objects.filter(cv1=first_industry,cv2=second_industry,company_country=area_country,company_province=area_province)[start_record : end_record]
        serializer = Get_Target_Pro_List_Serializer(get_target_pro_list_set,many=True)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#筛选获取需求列表
@api_view(['GET'])
def get_target_demand_list(request):
    c = {}
    c["message"]="Fail to get demand list"
    c["status"] = "fail"
    access_token = request.GET.get("access_token")
    mem_id = check_access_token(request)
    #company_tag = request.GET.get("company_tag") 可选
    first_industry = request.GET.get("first_industry")
    second_industry = request.GET.get("second_industry")#可选
    area_country = request.GET.get("area_country")
    area_province = request.GET.get("area_province")
    if mem_id:
        start_record, end_record = handle_page(request)
        get_target_demand_list_set = Demand.objects.filter(company_industries=first_industry,company_countries=area_country,company_provinces=area_province)[start_record : end_record]
        serializer = Get_Target_Demand_List_Serializer(get_target_demand_list_set,many=True)
     #   c["demand_company_industry"] = jsonpickle.pickler.encode(Demand.objects.filter(member_id=mem_id))
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#关键字搜索获取项目列表
@api_view(['GET'])
def get_keyword_search_pro_list(request):
    c = {}
    c["message"]="Fail to get pro list"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    keyword = request.GET.get("keyword")
    if mem_id:
        start_record, end_record = handle_page(request)
        get_keyword_search_pro_list_set = ProjectKeyword.objects.filter(keyword=keyword)[start_record : end_record]
        serializer = Get_Keyword_Search_Pro_List_Serializer(get_keyword_search_pro_list_set,many=True)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#消息主页获取与项目相关用户列表,获得需要建立一个最近联系人的表
@api_view(['GET'])
def get_pro_msg_list(request):
    c = {}
    c["message"]="Fail to get message list"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    if mem_id:
        start_record, end_record = handle_page(request)
        get_msg_list_set = Project.objects.filter()[start_record : end_record]
        serializer = Get_Pro_Msg_List_Serializer(get_msg_list_set,many=True)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#消息主页获取好友列表,需要建立一个最近联系人的表
@api_view(['GET'])
def get_friends_list(request):
    c = {}
    c["message"]="Fail to get friends list"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    if mem_id:
        start_record, end_record = handle_page(request)
        get_friends_list_set = Favorites.objects.filter(member_id=mem_id)[start_record : end_record]
        serializer = Get_Friends_List_Serializer(get_friends_list_set,many=True)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#获得项目Teaser列表
@api_view(['GET'])
def get_pro_teaser_list(request):
    c = {}
    c["data"]=""
    c["message"]="Fail to get user pro teaser list"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    if mem_id:
        start_record, end_record = handle_page(request)
        get_user_publish_pro_list_set = Project.objects.filter(member_id=mem_id)[start_record : end_record]
        serializer = Get_Pro_Teaser_List_Serializer(get_user_publish_pro_list_set,many=True)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#获得用户上传的文件列表
@api_view(['GET'])
def get_upload_file_list(request):
    c = {}
    c["data"]=""
    c["message"]="Fail to get user publish pro list"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    if mem_id:
        start_record, end_record = handle_page(request)
        get_upload_file_list_set = Project.objects.filter(member_id=mem_id)[start_record : end_record]
        serializer = Get_Upload_File_Serializer(get_upload_file_list_set,many=True)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#个人中心获得当前用户详情
@api_view(['GET'])
def get_personal_detail(request):
    c = {}
    c["data"]=""
    c["message"]="Fail to get user detail"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    if mem_id:
        get_personal_detail_set = Member.objects.get(pk=mem_id)
        serializer = Get_Personal_Detail_Serializer(get_personal_detail_set)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#获得当前用户发布的项目列表
@api_view(['GET'])
def get_personal_publish_pro_list(request):
    c = {}
    c["data"]=""
    c["message"]="Fail to get user publish pro list"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    if mem_id:
        start_record, end_record = handle_page(request)
        get_personal_publish_pro_list_set = Project.objects.filter(member_id=mem_id)[start_record : end_record]
        serializer = Get_Personal_Publish_Pro_List_Serializer(get_personal_publish_pro_list_set,many=True)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#获得当前用户关注的项目的列表
@api_view(['GET'])
def get_personal_care_pro_list(request):
    c = {}
    c["data"]=""
    c["message"]="Fail to get user care pro list"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    if mem_id:
        start_record, end_record = handle_page(request)
        get_user_care_pro_list_set = Favorites.objects.filter(member_id=mem_id)[start_record : end_record]
        serializer = Get_Personal_Care_Pro_List_Serializer(get_user_care_pro_list_set, many=True)
        favorites_member = Favorites.objects.filter(member_id=mem_id, type_relation=TypeFavorite.member)
        c["favorites_member"] = jsonpickle.pickler.encode(favorites_member)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#获得当前用户公司简介
@api_view(['GET'])
def get_personal_company_detail(request):
    c = {}
    c["message"]="Fail to get user care pro list"
    c["status"] = "fail"
    mem_id = check_access_token(request)
    if mem_id:
        get_personal_company_detail_set = Member.objects.get(pk=mem_id)
        serializer_company_data = Get_Personal_Company_Detail_Serializer(get_personal_company_detail_set)
        c["company_detail_data"] = serializer_company_data.data
        company_id = get_personal_company_detail_set.company_id
        company_members_set = Member.objects.filter(company_id=company_id)
        serializer_company_member_data = Get_Member_In_Same_Company_Serializer(company_members_set,many=True)
        c["company_member_data"] = serializer_company_member_data.data
        get_personal_publish_pro_list_set = Project.objects.filter(member_id=mem_id)
        serializer_publish_pro_set = Get_Personal_Publish_Pro_List_Serializer(get_personal_publish_pro_list_set,many=True)
        c["company_publish_pro_data"] = serializer_publish_pro_set.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#交易助手推荐的公司列表
@api_view(['GET'])
def genius_company_list(request):
    mem_id = check_access_token(request)
    c = {}
    c["message"]="Fail to get user care pro list"
    c["status"] = "fail"
    pro_id = request.GET.get("pro_id")
    if mem_id:
        start_record, end_record = handle_page(request)
        genius_company_list_set = RecommondItem.objects.filter(project_id=pro_id)[start_record:end_record]
        serializer = Genius_Company_List_Serializer(genius_company_list_set,many=True)
        c["recommended_company_number"] = genius_company_list_set.count()
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#交易助手筛选后的公司列表
@api_view(['GET'])
def genius_get_filter_buyer_list(request):
    mem_id = check_access_token(request)
    c = {}
    c["message"]="Fail to get user care pro list"
    c["status"] = "fail"
    pro_id = request.GET.get("pro_id")
    industry_id = request.GET.get("industry_id")
    country_id = request.GET.get("country_id")
    province_id = request.GET.get("province_id")
    reason = request.GET.get("reason")
    if mem_id:
        start_record, end_record = handle_page(request)
        company = Company.objects.filter(industry_id=industry_id,country_id=country_id,province_id=province_id)
        get_filter_buyer_list_set = RecommondItem.objects.filter(project_id=pro_id,company=company,target_reason=reason)[start_record:end_record]
        serializer = Genius_Get_Filter_Buyer_List_Serializer(get_filter_buyer_list_set,many=True)
        c["recommended_company_number"] = get_filter_buyer_list_set.count()
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#对交易助手推荐的公司操作
@api_view(['GET'])
def genius_company_operation(request):
    mem_id = check_access_token(request)
    c = {}
    c["message"]="Fail to operate"
    c["status"] = "fail"
    access_token = request.GET.get("access_token")
    mem = AccessToken.objects.get(access_token=access_token).member
    operation_type = request.GET.get("operation_type")
    item_id = request.GET.get("item_id")
    r = RecommondItem.objects.get(pk=item_id)
    if mem_id:
        p = ProjectTargetCompanyDetail()
        p.recommondItem = r
        if operation_type == '1':
            p.status = 1
            c["status"] = "success"
            c["message"] = "send project success"
        elif operation_type == '2':
            p.status = 0
            c["status"] = "success"
            c["message"] = "add to control panel success"
        p.company = r.company
        p.project = r.project
        p.member = mem
        p.save()
    r.is_in_control_panel = True
    r.save()
    return Response(c)

#管理面板显示与项目相关的公司列表及状态
@api_view(['GET'])
def get_controlboard_list(request):
    mem_id = check_access_token(request)
    c = {}
    c["message"]="Fail to get the list"
    c["status"] = "fail"
    pro_id = request.GET.get("pro_id")
    if mem_id:
        get_controlboard_detail_set = ProjectTargetCompanyDetail.objects.filter(project_id=pro_id)
        serializer =Get_Controlboard_List_Serializer(get_controlboard_detail_set,many=True)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#管理面板显示最近浏览项目的用户
@api_view(['GET'])
def get_controlboard_recent_view_pro_list(request):
    mem_id = check_access_token(request)
    c = {}
    c["message"]="Fail to get the users"
    c["status"] = "fail"
    pro_id = request.GET.get("pro_id")
    if mem_id:
        get_controlboard_list_set = Log.objects.filter(item_id=pro_id,operation_type=2,target_type=2)
        serializer =Get_Controlboard_Recent_View_Pro_List_Serializer(get_controlboard_list_set,many=True)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#管理面板显示最近收藏项目的用户
@api_view(['GET'])
def get_controlboard_recent_focuspro_list(request):
    mem_id = check_access_token(request)
    c = {}
    c["message"]="Fail to get the users"
    c["status"] = "fail"
    pro_id = request.GET.get("pro_id")
    if mem_id:
        get_controlboard_recent_focus_pro_list_set = Log.objects.filter(item_id=pro_id,operation_type=5,target_type=2)
        serializer =Get_Controlboard_Recent_Focus_Pro_List_Serializer(get_controlboard_recent_focus_pro_list_set,many=True)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)


#管理面板对列表中的公司进行操作
@api_view(['GET'])
def controlboard_company_operation(request):
    mem_id = check_access_token(request)
    c = {}
    c["message"]="Fail to operate"
    c["status"] = "fail"
    id = request.GET.get("id")
    operation_type = request.GET.get("operation_type")
    if mem_id:
        p = ProjectTargetCompanyDetail.objects.get(pk=id)
        if operation_type == '1':
            p.status = 1
            c["status"] = "success"
            c["message"] = "send project success"
        elif operation_type == '2':
            p.status = 2
            c["status"] = "success"
            c["message"] = "remove success"
        elif operation_type == '3':
            p.status = 3
            c["status"] = "success"
            c["message"] = "NDA Signed success"
        elif operation_type == '4':
            p.status = 4
            c["status"] = "success"
            c["message"] = "TS Signed success"
        elif operation_type == '5':
            p.status = 5
            c["status"] = "success"
            c["message"] = "Settlement success"
        p.save()
    return Response(c)

#管理面板添加新买家
@api_view(['GET'])
def get_newbuyer_list(request):
    mem_id = check_access_token(request)
    c = {}
    c["message"]="Fail to operate"
    c["status"] = "fail"
    keyword = request.GET.get("keyword")
    if mem_id and keyword !="":
        start_record, end_record = handle_page(request)
        get_newbuyer_list_set = Company.objects.filter(Q(name_en__icontains=keyword) | Q(name_cn__contains=keyword) | Q(short_name_en__icontains=keyword) | Q(short_name_cn__contains=keyword), Q(status=0) | Q(status=1) | Q(status=4))[start_record:end_record]
        serializer = Get_Newbuyer_List_Serializer(get_newbuyer_list_set,many=True)
        c["data"] = serializer.data
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#管理面板中发送项目给内部用户
@api_view(['POST'])
def send_pro_to_inneruser(request):
    mem_id = check_access_token(request)
    c = {}
    c["message"]="Fail to send pro to inner user"
    c["status"] = "fail"
    request_data = request.DATA
    if len(request_data) > 0:
        pro_id = request_data["pro_id"]
        project = Project.objects.get(id=pro_id)
        receiver_id = request_data["receiver_id"]
        receiver = Member.objects.get(id=receiver_id)
        receiver_email = receiver.email
        if mem_id and receiver_id:
            emailAccount = []
            dic = {}
            if receiver.fullname.strip():
                dic["userName"] = receiver.fullname
            dic["link"] = _get_project_link(pro_id)
            if project.name_cn.strip() != "":
                dic["projectName"] = project.name_cn
            else:
                dic["projectName"] = project.name_en
            html_content = loader.render_to_string("sales/"+request.lang+"/email_push.html", dic)
            emailAccount.append(receiver_email)
            title=_('NewChama Project Message')
            try:
                send_email_by_mq('email', 'email', title, set(emailAccount), html_content)
                c["status"] = "success"
                c["message"] = "ok"
            except Exception, e:
                msg = EmailMessage(title, html_content, EMAIL_HOST_USER, set(emailAccount))
                msg.content_subtype = "html"  # Main content is now textml
                msg.send()

            autoMsg = Message()
            autoMsg.project_id = pro_id
            autoMsg.type_relation = 1
            autoMsg.sender_id = mem_id
            autoMsg.receiver_id = receiver_id
            autoMsg.content = "您好，这是我的项目Teaser。若您对此感兴趣，欢迎与我取得联系。"
            autoMsg.save()
    return Response(c)

#管理面板中发送项目给外部用户,发送单个外部用户可以，但是多个好像只能成功发送第一个邮箱
@api_view(['POST'])
def send_pro_to_outerser(request):
    mem_id = check_access_token(request)
    c = {}
    c["message"]="Fail to send pro to outer user"
    c["status"] = "fail"
    email_list = []
    content_list = []
    title = "Newchama用户最新项目推荐"
    request_data = request.DATA
    if mem_id and len(request_data) > 0:
        try:
            pro_id = request_data["pro_id"]
            emails = request_data["other_email"]
            if pro_id:
                p = Project.objects.get(pk=pro_id)
                email_list = emails.split(";")
                dic = {}
                dic["p"] = p
                html_content = loader.render_to_string("sales/"+request.lang+"/email_extenal.html", dic)
                content_list.append(html_content)
                send_email_by_mq_multiple('email', 'email', title, email_list, content_list)
                member = get_object_or_404(Member,id=mem_id)
                c["status"] = "success"
                c["message"] = "ok"
        except Exception, e:
            try:
                for item in zip(email_list, content_list):
                    noPublishemail = []
                    noPublishemail.append(item[0])
                    msg = EmailMessage(title, item[1], EMAIL_HOST_USER, noPublishemail)
                    msg.content_subtype = "html"
                    msg.send()
                    logger.debug("send email successfully.")
            except Exception, e:
                logger.error(e.message)
            logger.error(e.message)
        if len(email_list) > 0:
            write_extenal_mail_log(request, member, p, email_list)
    return Response(c)

#偏好设置设置用户偏好行业
@api_view(['POST'])
def focus_aspect_setting(request):
    mem_id = check_access_token(request)
    m = Member.objects.get(pk=mem_id)
    c = {}
    c["message"]="Fail to set focus aspect"
    c["status"] = "fail"
    request_data = request.DATA
    if mem_id and len(request_data):
        industry_ids = request_data["industry_ids"]
        industry_id_list = industry_ids.split(",")
        m.focus_aspect = industry_id_list
        m.save()
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#偏好行业列表
@api_view(['GET'])
def get_focus_aspect_list(request):
    mem_id = check_access_token(request)
    c = {}
    c["message"]="Fail to set focus aspect"
    c["status"] = "fail"
    if mem_id:
        start_record, end_record = handle_page(request)
        get_focus_aspect_list_set = Industry.objects.filter(is_display=True)
        serializer = Get_Focus_Aspect_List_Serializer(get_focus_aspect_list_set,many=True)
        c["focus_aspect_data"] = serializer.data[start_record:end_record]
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)

#热门标签列表
@api_view(['GET'])
def get_hot_tag_list(request):
    mem_id = check_access_token(request)
    c = {}
    c["message"]="Fail to set focus aspect"
    c["status"] = "fail"
    if mem_id:
        start_record, end_record = handle_page(request)
        get_hot_tag_list_set = ProjectTag.objects.filter().all()
        serializer = Get_Hot_Tag_List_Serializer(get_hot_tag_list_set,many=True)
        c["hot_tag"] = serializer.data[start_record:end_record]
        c["status"] = "success"
        c["message"] = "ok"
    return Response(c)