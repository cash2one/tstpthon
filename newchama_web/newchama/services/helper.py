# -*- coding: utf-8 -*-  
from models import Country, Member, Industry, Favorites, TypeFavorite, Company, ConditionDemand, Demand, StatusDemand, StatusProject, \
    Message_Log
from models import Project, ConditionProject, Message, ProjectRecommendLog, DemandRecommendLog, TypeDemandRecommend,TypeProjectRecommend
from models import EditorSay
from log.models import Log, MemberDynamic
from django.db.models import Q
import base64
from newchama.settings import SECRET_SALT
import datetime


class Helper:

    def __init__(self):
        pass

    @staticmethod
    def find_countries():
        return Country.objects.all().order_by("-sort")

    @staticmethod
    def find_industries_by_father(father_id):
        return Industry.objects.filter(father_id=father_id)

    @staticmethod
    def find_industries_level1():
        return Industry.objects.filter(level=1, is_display=True)

    @staticmethod
    def find_industries_level2():
        return Industry.objects.filter(level=2, is_display=True).order_by("father")

    @staticmethod
    def find_member_favorite_project_ids(member_id):
        ids = []
        favorites = Favorites.objects.filter(member_id=member_id, type_relation=TypeFavorite.project)
        for f in favorites:
            ids.append(f.project.id)
        return ids

    @staticmethod
    def find_member_favorite_demand_ids(member_id):
        ids = []
        favorites = Favorites.objects.filter(member_id=member_id, type_relation=TypeFavorite.demand)
        for f in favorites:
            ids.append(f.demand.id)
        return ids

    #check the send company is exsit in MemberCompany
    @staticmethod
    def checkCompanyInMemberCompany(language, company_names, table_types):
        company = Company()
        exsit = []          #for member_company
        not_exsit_1 = []    #for repository_investmentcompany
        not_exsit_2 = []    #for repository_listedcompany
        for n, t in zip(company_names, table_types):
            if language == "en-us":
                company = Company.objects.filter(name_en=n).values("id")
            else:
                company = Company.objects.filter(name_cn=n).values("id")
            if company:
                exsit.append(company[0]["id"])
            else:
                if t == "2":
                    not_exsit_2.append(n)
                else:
                    not_exsit_1.append(n)
        # other_target_companies = not_exsit
        return exsit, not_exsit_1, not_exsit_2

    @staticmethod
    def hasAgentRole(company_type):
        if True:
            return False
        if company_type == 3:
            return True
        return False

    @staticmethod
    def url_encode(string):
        string = str(string) + SECRET_SALT
        data = base64.encodestring(string)
        data = data.replace("+", "_")
        data = data.replace("/", "-")
        data = data.replace("=", "")
        data = data.replace("\n", "")
        return data

    @staticmethod
    def url_decode(data):
        data = data.replace("_", "+")
        data = data.replace("-", "/")
        mod = len(data) % 4
        if mod:
            data += "===="[mod:4]
        string = base64.decodestring(data)
        string = string[0:(len(string)-len(SECRET_SALT))]
        return string

    @staticmethod
    def find_not_read_message(member_id):
        return Message.objects.filter(receiver_id=member_id,is_read=0,is_delete=0).order_by('-add_time').count()


    @staticmethod
    def find_dynamic_member(type_id, item_id):
        data = None
        if type_id == 0:
            data = Member.objects.get(pk=item_id)
        elif type_id == 1:
            p = Project.objects.get(pk=item_id)
            if p:
                data = p.member
        elif type_id == 2:
            d = Demand.objects.get(pk=item_id)
            if d:
                data = d.member
        return data


    #项目列表
    @staticmethod
    def find_timeline_project(startRecord, endRecord):
        data = Project.objects.filter(status=StatusProject.approved).order_by("-add_time")[startRecord: endRecord]
        return data

    #需求列表
    @staticmethod
    def find_timeline_demand(startRecord, endRecord):
        data = Demand.objects.filter(status=StatusDemand.approved).order_by("-add_time")[startRecord: endRecord]
        return data

    #xxx收藏了我的项目
    @staticmethod
    def find_timeline_project_favorite(member_id, startRecord, endRecord):
        data = Favorites.objects.filter(type_relation=1, project__member_id=member_id).order_by('-add_time')[startRecord: endRecord]
        return data

    #个人项目收藏需求
    @staticmethod
    def find_timeline_demand_favorite(member_id, startRecord, endRecord):
        data = Favorites.objects.filter(type_relation=2, demand__member_id=member_id).order_by('-add_time')[startRecord: endRecord]
        return data

    #个人在线留言
    @staticmethod
    def find_timeline_message(member_id, startRecord, endRecord):
        # data = Message.objects.filter(receiver_id=member_id,is_read=0).distinct().values("add_time", "sender__avatar", "sender__id", "sender__last_name", "sender__first_name").order_by('-add_time')[startRecord: endRecord]
        data = MemberDynamic.objects.filter(item_id=member_id, type=1).order_by("-update_time")[startRecord: endRecord]
        return data

    #个人被推送的项目
    @staticmethod
    def find_timeline_project_recommed(member_id, startRecord, endRecord):
        data = ProjectRecommendLog.objects.filter(type=TypeProjectRecommend.recommend, project__member_id=member_id).order_by('-add_time')[startRecord: endRecord]
        return data

    #个人被推送的需求
    @staticmethod
    def find_timeline_demand_recommend(member_id, startRecord, endRecord):
        data = DemandRecommendLog.objects.filter(type=TypeDemandRecommend.recommend, demand__member_id=member_id).order_by('-add_time')[startRecord: endRecord]
        return data

    #系统推荐项目
    @staticmethod
    def find_timeline_project_top(member_id, startRecord, endRecord):
        data = ProjectRecommendLog.objects.filter(type=TypeProjectRecommend.top, project__member_id=member_id).order_by('-add_time')[startRecord: endRecord]
        return data

    #系统推荐需求
    @staticmethod
    def find_timeline_demand_top(member_id, startRecord, endRecord):
        data = DemandRecommendLog.objects.filter(type=TypeDemandRecommend.top, demand__member_id=member_id).order_by('-add_time')[startRecord: endRecord]
        return data

    # newchama说
    @staticmethod
    def find_timeline_newchamasay(startRecord, endRecord):
        data = EditorSay.objects.order_by('-add_time')[startRecord: endRecord]
        return data

    #个人添加的项目
    @staticmethod
    def find_own_approve_project(member_id, startRecord, endRecord):
        data = Project.objects.filter(member_id=member_id, status=StatusProject.approved).order_by('-add_time')[startRecord: endRecord]
        return data

    #个人添加的需求
    @staticmethod
    def find_own_approve_demand(member_id, startRecord, endRecord):
        data = Demand.objects.filter(member_id=member_id, status=StatusDemand.approved).order_by('-add_time')[startRecord: endRecord]
        return data

    #个人查看的项目
    @staticmethod
    def find_own_log_project(member_id, startRecord, endRecord):
        # data = Log.objects.filter(user_id=member_id, operation_type=2, target_type=2).order_by('-time')[startRecord: endRecord]
        data = MemberDynamic.objects.filter(member_id=member_id, type=2).order_by("-update_time")[startRecord: endRecord]
        return data

    #个人查看的需求
    @staticmethod
    def find_own_log_demand(member_id, startRecord, endRecord):
        # data = Log.objects.filter(user_id=member_id, operation_type=2, target_type=3).order_by('-time')[startRecord: endRecord]
        data = MemberDynamic.objects.filter(member_id=member_id, type=3).order_by("-update_time")[startRecord: endRecord]
        return data

    # 我收藏的项目
    @staticmethod
    def find_own_favorite_project(member_id, startRecord, endRecord):
        data = Favorites.objects.filter(type_relation=1, member_id=member_id).order_by('-add_time')[startRecord: endRecord]
        return data

    #　我收藏的需求
    @staticmethod
    def find_own_favorite_demand(member_id, startRecord, endRecord):
        data = Favorites.objects.filter(type_relation=2, member_id=member_id).order_by('-add_time')[startRecord: endRecord]
        return data

    @staticmethod
    def checkCountMatch(count):
        if count > 100:
            return count / 10
        return count

    @staticmethod
    def update_message_log(message):
        ms_logs = Message_Log.objects.filter(sender=message.sender, receiver=message.receiver, item_type=message.type_relation).order_by("-id")
        if message.type_relation == 1:
            ms_logs = ms_logs.filter(item_id=message.project_id)
        elif message.type_relation == 2:
            ms_logs = ms_logs.filter(item_id=message.demand_id)
        if len(ms_logs) > 0:
            ms_log = ms_logs[0]
            ms_log.message = message
            ms_log.update_time = datetime.datetime.now()
            ms_log.save()
        else:
            ms_log = Message_Log()
            ms_log.sender = message.sender
            ms_log.receiver = message.receiver
            ms_log.message = message
            ms_log.item_type = message.type_relation
            if ms_log.item_type == 1:
                ms_log.item_id = message.project_id
            elif ms_log.item_type == 2:
                ms_log.item_id = message.demand_id
            ms_log.save()
