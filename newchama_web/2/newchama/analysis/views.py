#encoding:utf-8
from django.shortcuts import render, render_to_response, redirect, HttpResponse, RequestContext, get_object_or_404
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from newchama.decorators import login_required, permission_required
from newchama.helper import send_email_by_mq
from django.db.models import Q, connection
from member.models import Member,Company
from project.models import Project,ProjectViewLog
from demand.models import Demand,DemandViewLog,DemandTargetProjectDetail
from log.models import Log
from member_message.models import Message,Favorites
from tracking.models import TrackingItem
from analysis.models import AnalysisUserTotal,AnalysisUser,AnalysisProject,AnalysisProjectFinish
from newchama.settings import EMAIL_HOST_USER,IS_PRODUCT_HOST
from django.template import loader, Context
from django.core.mail import send_mail, EmailMessage
from adminuser.models import AdminUser
from recommond.models import RecommondItem, ProjectTargetCompanyDetail
import datetime
from django.db.models import Count

day_num=100
aDay = datetime.timedelta(days=1)
threeDay = datetime.timedelta(days=3)
sevenDay = datetime.timedelta(days=7)

@login_required
@permission_required("analysis")
def index(request):
    c={}
    today=datetime.date.today()-aDay
    
    for i in range(day_num):
        _time=today-aDay*i
        rec_num=AnalysisUserTotal.objects.filter(time=_time).count()
        if rec_num==0:
            
            rec = AnalysisUserTotal()
            rec.time = _time
            rec.user_num = get_user_num(_time+aDay)
            rec.project_num = get_project_num(_time+aDay)
            rec.demand_num = get_demand_num(_time+aDay)
            rec.listed_user_num = get_listed_user_num(_time+aDay)
            rec.unlisted_user_num = get_unlisted_user_num(_time+aDay)
            rec.vc_user_num = get_vc_user_num(_time+aDay)
            rec.fa_user_num = get_fa_user_num(_time+aDay)
            rec.save()

        


    c['result_list']=AnalysisUserTotal.objects.order_by('-time')

    return render_to_response("analysis/index.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def demand_detail(request):
    c={}
    
    _list=Demand.objects.filter(status=2).order_by('-id')
    for item in _list:
        item.send_num=DemandTargetProjectDetail.objects.filter(demand=item,is_delete=0).count()
        item.fav_num=Favorites.objects.filter(demand=item,type_relation=2).count()
        item.message_num=Message.objects.filter(demand=item,type_relation=2).count()
        item.view_num=DemandViewLog.objects.filter(demand=item).count()
        item.man_recommond_num=0
        item.man_recommond_click_num=0
        item.machine_recommond_num=0
        item.machine_recommond_click_num=0

        
    download = request.GET.get("download", "")
    if download != "":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="demand_detail.csv"'
        t = loader.get_template('analysis/project_detail_download_template.txt')
        d = Context({
            'result_list': _list,
        })
        response.write(t.render(d))
        return response    

    c['result_list']=_list

    return render_to_response("analysis/demand_detail.html", c, context_instance=RequestContext(request))

@login_required
@permission_required("analysis")
def demand(request):
    c={}
    today=datetime.date.today()-aDay
    
    for i in range(day_num):
        _time=today-aDay*i
        rec_num=AnalysisProject.objects.filter(time=_time,type=1).count()
        if rec_num==0:
            
            rec = AnalysisProject()
            rec.time = _time
            rec.type=1
            rec.all_num = get_demand_num(_time+aDay)
            rec.valid_num = get_demand_valid_num(_time+aDay)
            rec.created_num = get_demand_created_num(_time+aDay)
            rec.audit_num = get_demand_audit_num(_time+aDay)
            rec.offline_num = get_demand_offline_num(_time+aDay)
            rec.pendding_num = get_demand_pendding_num(_time+aDay)
            rec.draft_num = get_demand_draft_num(_time+aDay)
            rec.user_add_num = get_demand_user_add_num(_time+aDay)
            rec.bd_add_num = get_demand_bd_add_num(_time+aDay)
            rec.target_num = get_demand_target_num(_time+aDay)
            rec.public_num = get_demand_public_num(_time+aDay)
            
            rec.save()

    c['result_list']=AnalysisProject.objects.filter(type=1).order_by('-time')

    return render_to_response("analysis/demand.html", c, context_instance=RequestContext(request))

@login_required
@permission_required("analysis")
def demand_target(request,id):
    c={}
    demand=get_object_or_404(Demand,pk=id)
    c['result_list']=DemandTargetProjectDetail.objects.filter(demand=demand,is_delete=0).order_by('-id')

    return render_to_response("analysis/target_detail_demand.html", c, context_instance=RequestContext(request))



@login_required
@permission_required("analysis")
def demand_view(request,id):
    c={}
    demand=get_object_or_404(Demand,pk=id)
    c['result_list']=DemandViewLog.objects.filter(demand=demand).order_by('-id')

    return render_to_response("analysis/view_detail.html", c, context_instance=RequestContext(request))

@login_required
@permission_required("analysis")
def demand_fav(request,id):
    c={}
    demand=get_object_or_404(Demand,pk=id)
    c['result_list']=Favorites.objects.filter(demand=demand,type_relation=2).order_by('-id')

    return render_to_response("analysis/fav_detail.html", c, context_instance=RequestContext(request))

@login_required
@permission_required("analysis")
def demand_message(request,id):
    c={}
    demand=get_object_or_404(Demand,pk=id)
    c['result_list']=Message.objects.filter(demand=demand,type_relation=2).order_by('-id')

    return render_to_response("analysis/message_detail.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def project_detail(request):
    c={}
    
    _list=Project.objects.filter(status=2).order_by('-id')
    for item in _list:
        item.send_num=ProjectTargetCompanyDetail.objects.filter(project=item,is_delete=0,status=1).count()
        item.control_panel_num=ProjectTargetCompanyDetail.objects.filter(project=item,is_delete=0).exclude(status=1).count()
        item.fav_num=Favorites.objects.filter(project=item,type_relation=1).count()
        item.message_num=Message.objects.filter(project=item,type_relation=1).count()
        item.view_num=ProjectViewLog.objects.filter(project=item).count()
        item.man_recommond_num=RecommondItem.objects.filter(project=item,is_man=True,is_delete=False).count()
        item.man_recommond_click_num=Log.objects.filter(operation_type=2,target_type=5,detail_type=5,memo=item.id).count()
        item.machine_recommond_num=RecommondItem.objects.filter(project=item,is_man=False,is_delete=False).count()
        item.machine_recommond_click_num=Log.objects.filter(operation_type=2,target_type=5,detail_type=6,memo=item.id).count()

    download = request.GET.get("download", "")
    if download != "":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="project_detail.csv"'
        t = loader.get_template('analysis/project_detail_download_template.txt')
        d = Context({
            'result_list': _list,
        })
        response.write(t.render(d))
        return response
    c['result_list']=_list

    return render_to_response("analysis/project_detail.html", c, context_instance=RequestContext(request))



@login_required
@permission_required("analysis")
def demand_finish(request):
    c={}
    today=datetime.date.today()-aDay
    
    for i in range(day_num):
        _time=today-aDay*i
        rec_num=AnalysisProjectFinish.objects.filter(time=_time,type=1).count()
        if rec_num==0:
            
            rec = AnalysisProjectFinish()
            rec.time = _time
            rec.type=1
            rec.all_num = get_project_num(_time+aDay)
            rec.rang_num_1_cn = get_demand_rang_num(_time+aDay,1,0)
            rec.rang_num_2_cn = get_demand_rang_num(_time+aDay,2,0)
            rec.rang_num_3_cn = get_demand_rang_num(_time+aDay,3,0)
            rec.rang_num_4_cn = get_demand_rang_num(_time+aDay,4,0)
            rec.rang_num_1_en = get_demand_rang_num(_time+aDay,1,1)
            rec.rang_num_2_en = get_demand_rang_num(_time+aDay,2,1)
            rec.rang_num_3_en = get_demand_rang_num(_time+aDay,3,1)
            rec.rang_num_4_en = get_demand_rang_num(_time+aDay,4,1)
            rec.save()

    c['result_list']=AnalysisProjectFinish.objects.filter(type=1).order_by('-time')

    return render_to_response("analysis/demand_finish.html", c, context_instance=RequestContext(request))




@login_required
@permission_required("analysis")
def project_finish(request):
    c={}
    today=datetime.date.today()-aDay
    
    for i in range(day_num):
        _time=today-aDay*i
        rec_num=AnalysisProjectFinish.objects.filter(time=_time,type=0).count()
        if rec_num==0:
            
            rec = AnalysisProjectFinish()
            rec.time = _time
            rec.type=0
            rec.all_num = get_project_num(_time+aDay)
            rec.rang_num_1_cn = get_project_rang_num(_time+aDay,1,0)
            rec.rang_num_2_cn = get_project_rang_num(_time+aDay,2,0)
            rec.rang_num_3_cn = get_project_rang_num(_time+aDay,3,0)
            rec.rang_num_4_cn = get_project_rang_num(_time+aDay,4,0)
            rec.rang_num_1_en = get_project_rang_num(_time+aDay,1,1)
            rec.rang_num_2_en = get_project_rang_num(_time+aDay,2,1)
            rec.rang_num_3_en = get_project_rang_num(_time+aDay,3,1)
            rec.rang_num_4_en = get_project_rang_num(_time+aDay,4,1)
            rec.save()

    c['result_list']=AnalysisProjectFinish.objects.filter(type=0).order_by('-time')

    return render_to_response("analysis/project_finish.html", c, context_instance=RequestContext(request))




@login_required
@permission_required("analysis")
def project(request):
    c={}
    today=datetime.date.today()-aDay
    
    for i in range(day_num):
        _time=today-aDay*i
        rec_num=AnalysisProject.objects.filter(time=_time,type=0).count()
        if rec_num==0:
            
            rec = AnalysisProject()
            rec.time = _time
            rec.type=0
            rec.all_num = get_project_num(_time+aDay)
            rec.valid_num = get_project_valid_num(_time+aDay)
            rec.created_num = get_project_created_num(_time+aDay)
            rec.audit_num = get_project_audit_num(_time+aDay)
            rec.offline_num = get_project_offline_num(_time+aDay)
            rec.pendding_num = get_project_pendding_num(_time+aDay)
            rec.draft_num = get_project_draft_num(_time+aDay)
            rec.user_add_num = get_project_user_add_num(_time+aDay)
            rec.bd_add_num = get_project_bd_add_num(_time+aDay)
            rec.target_num = get_project_target_num(_time+aDay)
            rec.public_num = get_project_public_num(_time+aDay)
            rec.save()

    c['result_list']=AnalysisProject.objects.filter(type=0).order_by('-time')

    return render_to_response("analysis/project.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def project_target(request,id):
    c={}
    project=get_object_or_404(Project,pk=id)

    _list=ProjectTargetCompanyDetail.objects.filter(project=project,is_delete=0).order_by('-id')
    for item in _list:
        recommond_num=RecommondItem.objects.filter(project=project,company=item.company,is_delete=0).count()
        if recommond_num>0:
            _recommond=RecommondItem.objects.filter(project=project,company=item.company,is_delete=0).first()
            item.recommend_all_score=_recommond.sum_score
            item.recommend_project_score=_recommond.sum_project_score
            item.recommend_company_score=_recommond.sum_company_score
            item.is_man = _recommond.is_man

    c['result_list']=_list

    return render_to_response("analysis/target_detail.html", c, context_instance=RequestContext(request))



@login_required
@permission_required("analysis")
def project_view(request,id):
    c={}
    project=get_object_or_404(Project,pk=id)
    c['result_list']=ProjectViewLog.objects.filter(project=project).order_by('-id')

    return render_to_response("analysis/view_detail.html", c, context_instance=RequestContext(request))

@login_required
@permission_required("analysis")
def project_recommond_view(request,id):
    c={}
    
    c['result_list_man']=Log.objects.filter(operation_type=2,target_type=5,detail_type=5,memo=id).order_by('-id')

    c['result_list_machine']=Log.objects.filter(operation_type=2,target_type=5,detail_type=6,memo=id).order_by('-id')

    return render_to_response("analysis/project_recommond_view.html", c, context_instance=RequestContext(request))




@login_required
@permission_required("analysis")
def project_fav(request,id):
    c={}
    project=get_object_or_404(Project,pk=id)

    c['result_list']=Favorites.objects.filter(project=project,type_relation=1).order_by('-id')

    return render_to_response("analysis/fav_detail.html", c, context_instance=RequestContext(request))

@login_required
@permission_required("analysis")
def project_message(request,id):
    c={}
    project=get_object_or_404(Project,pk=id)

    c['result_list']=Message.objects.filter(project=project,type_relation=1).order_by('-id')

    return render_to_response("analysis/message_detail.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def user(request):
    c={}
    today=datetime.date.today()-aDay
    
    for i in range(day_num):
        _time=today-aDay*i
        rec_num=AnalysisUser.objects.filter(time=_time).count()
        if rec_num==0:
            
            rec = AnalysisUser()
            rec.time = _time
            rec.logined_user_num = get_login_user_num(_time+aDay)
            rec.add_user_num = get_add_user_num(_time+aDay)
            rec.created_project_user_num = get_created_project_user_num(_time+aDay)
            rec.created_demand_user_num = get_created_demand_user_num(_time+aDay)
            rec.unpublish_user_num = get_unpublish_user_num(_time+aDay)
            rec.sendmail_user_num = get_sendmail_user_num(_time+aDay)
            rec.visited_index_user_num = get_visited_index_user_num(_time+aDay)
            rec.active_user_num = get_active_user_num(_time+aDay)
            rec.target_user_num = get_target_user_num(_time+aDay)

            rec.save()

        
    c['result_list']=AnalysisUser.objects.order_by('-time')

    return render_to_response("analysis/user.html", c, context_instance=RequestContext(request))



@login_required
@permission_required("analysis")
def user_detail(request):
    c={}
    c['result_list']=Member.objects.exclude(status=5).order_by('-id')

    for item in c['result_list']:

        item.login_num=Log.objects.filter(user=item,operation_type=1).count()
        item.view_project_num=Log.objects.filter(user=item,operation_type=2,target_type=2).count()
        item.view_demand_num=Log.objects.filter(user=item,operation_type=2,target_type=3).count()
        item.send_message_num=Message.objects.filter(sender=item,is_delete=0).count()
        item.send_project_num=Project.objects.exclude(status=5).filter(member=item).count()
        item.send_demand_num=Demand.objects.exclude(status=5).filter(member=item).count()
        item.fav_project_num=Favorites.objects.filter(member=item,type_relation=1).count()
        item.fav_demand_num=Favorites.objects.filter(member=item,type_relation=2).count()

    download = request.GET.get("download", "")
    if download != "":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_detail.csv"'
        t = loader.get_template('analysis/user_detail_download_template.txt')
        d = Context({
            'result_list': c['result_list'],
        })
        response.write(t.render(d).encode('gb18030'))
        return response

    return render_to_response("analysis/user_detail.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def user_detail_login(request,id):
    c={}
    user=get_object_or_404(Member,pk=id)
    c['result_list']=Log.objects.filter(user=user,operation_type=1).order_by('-id')

    return render_to_response("analysis/user_detail_login.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def user_detail_view_project(request,id):
    c={}
    user=get_object_or_404(Member,pk=id)
    c['result_list']=Log.objects.filter(user=user,operation_type=2,target_type=2).order_by('-id')

    return render_to_response("analysis/user_detail_view_project.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def user_detail_view_demand(request,id):
    c={}
    user=get_object_or_404(Member,pk=id)
    c['result_list']=Log.objects.filter(user=user,operation_type=2,target_type=3).order_by('-id')

    return render_to_response("analysis/user_detail_view_demand.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def user_detail_send_message(request,id):
    c={}
    user=get_object_or_404(Member,pk=id)
    c['result_list']=Message.objects.filter(sender=user,is_delete=0).order_by('-id')

    return render_to_response("analysis/user_detail_send_message.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def user_detail_send_project(request,id):
    c={}
    user=get_object_or_404(Member,pk=id)
    c['result_list']=Project.objects.exclude(status=5).filter(member=user).order_by('-id')

    return render_to_response("analysis/user_detail_send_project.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def user_detail_send_demand(request,id):
    c={}
    user=get_object_or_404(Member,pk=id)
    c['result_list']=Demand.objects.exclude(status=5).filter(member=user).order_by('-id')

    return render_to_response("analysis/user_detail_send_demand.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def user_detail_fav_project(request,id):
    c={}
    user=get_object_or_404(Member,pk=id)
    c['result_list']=Favorites.objects.filter(member=user,type_relation=1).order_by('-id')

    return render_to_response("analysis/user_detail_fav_project.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def user_detail_fav_demand(request,id):
    c={}
    user=get_object_or_404(Member,pk=id)
    c['result_list']=Favorites.objects.filter(member=user,type_relation=2).order_by('-id')

    return render_to_response("analysis/user_detail_fav_demand.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def get_collected_number(request):
    c={}
    collected_count = Favorites.objects.count()
    cursor = connection.cursor()
    sql_ = "select count(*) from project_project_target_companies"
    cursor.execute(sql_)
    recommond_count = cursor.fetchone()[0]
    project = Project.target_companies
    c['collected_count']=collected_count
    c['recommond_count']= recommond_count
    return render_to_response("analysis/get_collected_number.html",c,context_instance=RequestContext(request))

@login_required
@permission_required("analysis")
def action(request):
    
    return redirect('analysis.action_message')



@login_required
@permission_required("analysis")
def action_message(request):
    c={}
    _member_id_list = Message.objects.filter(is_read=0,is_delete=0).values('receiver_id').distinct()
    _member_id_list1=[item['receiver_id'] for item in _member_id_list]

    _member_list =Member.objects.filter(id__in=_member_id_list1).order_by('-id')
    for member in _member_list:
        _tracking_num = TrackingItem.objects.filter(tracking_id=member.id,tracking_type=1,content='给用户发送过未读消息提醒').order_by('-add_time').count()
        if _tracking_num >0:

            _tracking_item=TrackingItem.objects.filter(tracking_id=member.id,tracking_type=1,content='给用户发送过未读消息提醒').order_by('-add_time').first()
            member.send_time=_tracking_item.add_time
        
    
    c['result_list']=_member_list
    return render_to_response("analysis/action_message.html", c, context_instance=RequestContext(request))




@login_required
@permission_required("analysis")
def action_publish(request):
    c={}
    _member_id_list1 = Project.objects.exclude(status=5).filter(update_time__gt=datetime.date.today()-sevenDay).values('member_id').distinct()
    _member_id_list2 = Demand.objects.exclude(status=5).filter(update_time__gt=datetime.date.today()-sevenDay).values('member_id').distinct()


    _member_id_list3=[item['member_id'] for item in _member_id_list1]
    _member_id_list4=[item['member_id'] for item in _member_id_list2]
    _member_id_list=set(_member_id_list3+_member_id_list4)
    print _member_id_list
    print '*'*80

    _member_list =Member.objects.exclude(id__in=_member_id_list).filter(status=1).order_by('-id')
    for member in _member_list:
        _tracking_num = TrackingItem.objects.filter(tracking_id=member.id,tracking_type=1,content='给用户发送过未发布项目消息提醒').count()
        if _tracking_num >0:

            _tracking_item=TrackingItem.objects.filter(tracking_id=member.id,tracking_type=1,content='给用户发送过未发布项目消息提醒').order_by('-add_time').first()
            member.send_time=_tracking_item.add_time
    
    c['result_list']=_member_list
    return render_to_response("analysis/action_publish.html", c, context_instance=RequestContext(request))




@login_required
@permission_required("analysis")
def action_login(request):
    c={}
    _member_list = Member.objects.filter(last_login_time__lt=datetime.date.today()-threeDay,status=1).order_by('-id')
    
    for member in _member_list:
        _tracking_num = TrackingItem.objects.filter(tracking_id=member.id,tracking_type=1,content='给用户发送过未登录消息提醒').count()
        if _tracking_num >0:

            _tracking_item=TrackingItem.objects.filter(tracking_id=member.id,tracking_type=1,content='给用户发送过未登录消息提醒').order_by('-add_time').first()
            member.send_time=_tracking_item.add_time
    
    c['result_list']=_member_list
    return render_to_response("analysis/action_login.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def send_mail_user(request,id):
    c={}
    rec=get_object_or_404(AnalysisUser,pk=id)
    _time=rec.time
    c['result_list']=ProjectTargetCompanyDetail.objects.filter(is_delete=False,add_time__lt=(_time+aDay),add_time__gte=(_time)).order_by('-add_time')
    return render_to_response("analysis/send_mail_user.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def no_creat_user(request,id):
    c={}
    rec=get_object_or_404(AnalysisUser,pk=id)
    c['result_list']=list(get_unpublish_user(rec.time+aDay))
    return render_to_response("analysis/login_user.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def login_user(request,id):
    c={}
    rec=get_object_or_404(AnalysisUser,pk=id)
    c['result_list']=get_login_user(rec.time+aDay)
    return render_to_response("analysis/login_user.html", c, context_instance=RequestContext(request))


@permission_required("analysis")
def active_user(request,id):
    c={}
    rec=get_object_or_404(AnalysisUser,pk=id)
    c['result_list']=get_active_user(rec.time+aDay)
    return render_to_response("analysis/login_user.html", c, context_instance=RequestContext(request))



@login_required
@permission_required("analysis")
def visited_index_user(request,id):
    c={}
    rec=get_object_or_404(AnalysisUser,pk=id)
    c['result_list']=get_visited_index_user(rec.time+aDay)
    return render_to_response("analysis/login_user.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def add_user(request,id):
    c={}
    rec=get_object_or_404(AnalysisUser,pk=id)
    c['result_list']=get_add_user(rec.time+aDay)
    return render_to_response("analysis/login_user.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def creat_project_user(request,id):
    c={}
    rec=get_object_or_404(AnalysisUser,pk=id)
    c['result_list']=get_created_project_user(rec.time+aDay)
    return render_to_response("analysis/login_user.html", c, context_instance=RequestContext(request))



@login_required
@permission_required("analysis")
def creat_demand_user(request,id):
    c={}
    rec=get_object_or_404(AnalysisUser,pk=id)
    c['result_list']=get_created_demand_user(rec.time+aDay)
    return render_to_response("analysis/login_user.html", c, context_instance=RequestContext(request))



@login_required
@permission_required("analysis")
def message_list(request):
    c={}
    message_list = Message.objects.all().order_by("project", "demand")
    par_id = 0
    result = []
    for i, m in enumerate(message_list):
        if m.project:
            type = "项目"
            title = m.project.name_cn
            id = m.project_id
        elif m.demand:
            type = "需求"
            id = m.demand_id
            title = m.demand.name_cn
        if m.project or m.demand:
            if i == 0 or id != par_id:
                message = []
                msgs = []
                for m2 in message_list:
                    if m2.project == m.project:
                        msgs.append(str(m2.sender) + " - " + str(m2.receiver))
                par_id = id
                message.append(type)
                message.append(title)
                message.append(msgs)
                result.append(message)
    c["result"] = result

    return render_to_response("analysis/message_list.html", c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required("analysis")
def send_message_noread_mail(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            
            member=Member.objects.get(pk=id)
            message_list = Message.objects.filter(is_read=0,is_delete=0,receiver=member)

            message_num =message_list.count()
            plist=[]

            if message_num >0:
                for m in message_list:
                    if m.type_relation==1:
                        plist.append(m.project)

                    if m.type_relation==2:
                        plist.append(m.demand)
            plist=list(set(plist))[0:3]
            if IS_PRODUCT_HOST:
                _send_message_email(member.email,member.first_name,message_num,plist)
            else:

                _send_message_email('richard@newchama.com',member.first_name,message_num,plist)
            


            _tracking = TrackingItem()
            _tracking.tracking_type=1
            _tracking.tracking_id=member.id
            _tracking.tracking_name=member.first_name
            _tracking.content="给用户发送过未读消息提醒"

            uid = request.session['uid']
            admin_user=get_object_or_404(AdminUser,id=uid)
            _tracking.user = admin_user

            _tracking.save()



            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)



@csrf_exempt
@login_required
@permission_required("analysis")
def send_message_nopublish_mail(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            
            member=Member.objects.get(pk=id)
           
            if IS_PRODUCT_HOST:
                _send_publish_message_email(member.email,member.first_name)
            else:

                _send_publish_message_email('richard@newchama.com',member.first_name)
            

            _tracking = TrackingItem()
            _tracking.tracking_type=1
            _tracking.tracking_id=member.id
            _tracking.tracking_name=member.first_name
            _tracking.content="给用户发送过未发布项目消息提醒"

            uid = request.session['uid']
            admin_user=get_object_or_404(AdminUser,id=uid)
            _tracking.user = admin_user

            _tracking.save()



            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)



@csrf_exempt
@login_required
@permission_required("analysis")
def send_message_nologin_mail(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            
            member=Member.objects.get(pk=id)
            

            if member.company.type in [1,3,5]:
                is_sales=True
                plist=Demand.objects.filter(status=2).order_by('-id')[0:3]
            else:
                is_sales=False
                plist=Project.objects.filter(status=2).order_by('-id')[0:3]
            
            if IS_PRODUCT_HOST:
                _send_login_message_email(member.email,is_sales,plist)
            else:

                _send_login_message_email('richard@newchama.com',is_sales,plist)
            


            _tracking = TrackingItem()
            _tracking.tracking_type=1
            _tracking.tracking_id=member.id
            _tracking.tracking_name=member.first_name
            _tracking.content="给用户发送过未登录消息提醒"

            uid = request.session['uid']
            admin_user=get_object_or_404(AdminUser,id=uid)
            _tracking.user = admin_user

            _tracking.save()



            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


def _send_message_email(email,name,message_num,plist):

    mail_dic = dict()
    mail_dic['email'] = email
    mail_dic['message_num'] = message_num
    mail_dic['name'] = name
    mail_dic['plist'] = plist

    html_content = loader.render_to_string("analysis/email_has_noread_message.html", mail_dic)

    title=u'NewChama用户未读邮件通知'
    try:
       
        send_email_by_mq('email','email',title,email,html_content)

    except Exception, e:
        msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [email])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()


def _send_publish_message_email(email,name):
    mail_dic = dict()
    mail_dic['email'] = email
    mail_dic['name'] = name

    html_content = loader.render_to_string("analysis/email_has_nopublish_message.html", mail_dic)


    title=u'NewChama用户未发送项目邮件通知'
    try:
       
        send_email_by_mq('email','email',title,email,html_content)

    except Exception, e:
        msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [email])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()




def _send_login_message_email(email,is_sales,plist):
    mail_dic = dict()
    mail_dic['email'] = email
    
    mail_dic['is_sales'] = is_sales
    mail_dic['list'] = plist

    html_content = loader.render_to_string("analysis/email_has_nologin_message.html", mail_dic)

    title=u'NewChama用户未登录邮件通知'
    try:
       
        send_email_by_mq('email','email',title,email,html_content)

    except Exception, e:
        msg = EmailMessage(title, html_content, EMAIL_HOST_USER, [email])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()


def get_user_num(date):
    return Member.objects.filter(add_time__lt=date).count()

def get_listed_user_num(date):
    return Member.objects.filter(company__type=1,add_time__lt=date).count()

def get_unlisted_user_num(date):
    return Member.objects.filter(company__type=2,add_time__lt=date).count()

def get_vc_user_num(date):
    return Member.objects.filter(company__type=3,add_time__lt=date).count()

def get_fa_user_num(date):
    return Member.objects.filter(company__type=4,add_time__lt=date).count()

def get_project_num(date):
    return Project.objects.exclude(status=5).filter(add_time__lt=date).count()


def get_project_rang_num(date,range,language):
    _min_range=0
    _max_range=100

    if range==1:
        _min_range=0
        _max_range=30
    
    if range==2:
        _min_range=30
        _max_range=50

    if range==3:
        _min_range=50
        _max_range=80

    if range==4:
        _min_range=80
        _max_range=100

    if language==0:
        return Project.objects.exclude(status=5).filter(add_time__lt=date,integrity__gte=_min_range,integrity__lt=_max_range).count()
    else:
        return Project.objects.exclude(status=5).filter(add_time__lt=date,integrity_en__gte=_min_range,integrity_en__lt=_max_range).count()


def get_demand_rang_num(date,range,language):
    _min_range=0
    _max_range=100

    if range==1:
        _min_range=0
        _max_range=30
    
    if range==2:
        _min_range=30
        _max_range=50

    if range==3:
        _min_range=50
        _max_range=80

    if range==4:
        _min_range=80
        _max_range=100

    if language==0:
        return Demand.objects.exclude(status=5).filter(add_time__lt=date,integrity__gt=_min_range,integrity__lt=_max_range).count()
    else:
        return Demand.objects.exclude(status=5).filter(add_time__lt=date,integrity_en__gt=_min_range,integrity_en__lt=_max_range).count()




def get_project_valid_num(date):
    return Project.objects.filter(status=2,add_time__lt=date,expire_date__gt=date).count()

def get_project_created_num(date):
    return Project.objects.exclude(status=5).filter(add_time__lt=date,add_time__gte=(date-aDay)).count()


def get_project_audit_num(date):
    return Project.objects.filter(add_time__lt=date,status=2).count()


def get_project_offline_num(date):
    return Project.objects.filter(add_time__lt=date,status=3).count()

def get_project_pendding_num(date):
    return Project.objects.filter(add_time__lt=date,status=0).count()

def get_project_draft_num(date):
    return Project.objects.filter(add_time__lt=date,status=4).count()


def get_project_user_add_num(date):
    return Project.objects.exclude(status=5).filter(add_time__lt=date).count()

def get_project_bd_add_num(date):
    return 0

def get_project_target_num(date):
    
    return Project.objects.exclude(status=5).filter(is_suitor=True,add_time__lt=date).count()

def get_project_public_num(date):
    return Project.objects.exclude(status=5).filter(is_suitor=False,add_time__lt=date).count()


def get_demand_num(date):
    return Demand.objects.exclude(status=5).filter(add_time__lt=date).count()


def get_demand_valid_num(date):
    return Demand.objects.filter(status=2,add_time__lt=date,expire_date__gt=date).count()

def get_demand_created_num(date):
    return Demand.objects.exclude(status=5).filter(add_time__lt=date,add_time__gte=(date-aDay)).count()


def get_demand_audit_num(date):
    return Demand.objects.filter(add_time__lt=date,status=2).count()


def get_demand_offline_num(date):
    return Demand.objects.filter(add_time__lt=date,status=3).count()

def get_demand_pendding_num(date):
    return Demand.objects.filter(add_time__lt=date,status=0).count()

def get_demand_draft_num(date):
    return Demand.objects.filter(add_time__lt=date,status=4).count()


def get_demand_user_add_num(date):
    return Demand.objects.exclude(status=5).filter(add_time__lt=date).count()

def get_demand_bd_add_num(date):
    return 0

def get_demand_target_num(date):
    
    return Demand.objects.exclude(status=5).filter(is_suitor=True,add_time__lt=date).count()


def get_demand_public_num(date):
    return Demand.objects.exclude(status=5).filter(is_suitor=False,add_time__lt=date).count()


def get_login_user_num(date):
    return Log.objects.filter(operation_type=1,target_type=1,time__lt=date,time__gte=(date-aDay)).values('user_id').distinct().count()


def get_login_user(date):
    temp_list=Log.objects.filter(operation_type=1,target_type=1,time__lt=date,time__gte=(date-aDay)).values('user_id').distinct()
    id_list=[item['user_id'] for item in temp_list]

    return Member.objects.filter(pk__in=id_list)


def get_target_user_num(date):

    _num=0
    company_id_list=ProjectTargetCompanyDetail.objects.filter(add_time__lt=date,add_time__gte=(date-aDay)).values('company_id').distinct()
    company_list=Company.objects.filter(pk__in=company_id_list)
    for c in company_list:
        _num += c.member_set.count()
    return _num

def get_active_user_num(date):
    temp_list = Log.objects.filter(operation_type=1,target_type=1,time__lt=date,time__gte=(date-datetime.timedelta(days=30))).values('user_id').distinct()
    
    id_list=[item['user_id'] for item in temp_list]
    _num=0
    for uid in id_list:
        if Log.objects.filter(operation_type=1,target_type=1,time__lt=date,time__gte=(date-datetime.timedelta(days=30)),user__id=uid).count()>=3:
            _num +=1
    return _num


def get_active_user(date):
    temp_list=Log.objects.filter(operation_type=1,target_type=1,time__lt=date,time__gte=(date-datetime.timedelta(days=30))).values('user_id').distinct()
    id_list=[item['user_id'] for item in temp_list]

    _tlist=[]
    for uid in id_list:
        if Log.objects.filter(operation_type=1,target_type=1,time__lt=date,time__gte=(date-datetime.timedelta(days=30)),user__id=uid).count()>=3:
            _tlist.append(Member.objects.get(pk=uid))

    return _tlist



def get_visited_index_user_num(date):
    return Log.objects.filter(operation_type=2,target_type=8,time__lt=date,time__gte=(date-aDay)).values('user_id').distinct().count()


def get_visited_index_user(date):
    temp_list=Log.objects.filter(operation_type=2,target_type=8,time__lt=date,time__gte=(date-aDay)).values('user_id').distinct()
    id_list=[item['user_id'] for item in temp_list]

    return Member.objects.filter(pk__in=id_list)




def get_add_user_num(date):
    return Member.objects.filter(Q(status=1) | Q(status=2),add_time__lt=date,add_time__gte=(date-aDay)).count()

def get_add_user(date):
    return Member.objects.filter(Q(status=1) | Q(status=2),add_time__lt=date,add_time__gte=(date-aDay))



def get_created_project_user_num(date):
    return Project.objects.exclude(status=5).filter(add_time__lt=date,add_time__gte=(date-aDay)).values('member_id').distinct().count()


def get_created_project_user(date):
    temp_list = Project.objects.exclude(status=5).filter(add_time__lt=date,add_time__gte=(date-aDay)).values('member_id').distinct()
    id_list=[item['member_id'] for item in temp_list]
    return Member.objects.filter(pk__in=id_list)


def get_created_demand_user_num(date):
    return Demand.objects.exclude(status=5).filter(add_time__lt=date,add_time__gte=(date-aDay)).values('member_id').distinct().count()


def get_created_demand_user(date):
    temp_list = Demand.objects.exclude(status=5).filter(add_time__lt=date,add_time__gte=(date-aDay)).values('member_id').distinct()
    id_list=[item['member_id'] for item in temp_list]
    return Member.objects.filter(pk__in=id_list)


def get_unpublish_user_num(date):
    num=0
    login_num=get_login_user_num(date)
    created_project_user=Project.objects.exclude(status=5).filter(add_time__lt=date,add_time__gte=(date-aDay)).values('member_id').distinct()
    created_demand_user=Demand.objects.exclude(status=5).filter(add_time__lt=date,add_time__gte=(date-aDay)).values('member_id').distinct()

    _list=[]
    for item in created_project_user:
        _list.append(item['member_id'])

    for item in created_demand_user:
        _list.append(item['member_id'])

    num=login_num-len(set(_list))
    if num<0:
        num=0
    return num

def get_unpublish_user(date):
    num=0
    login_user_list=get_login_user(date)
    created_project_user=get_created_project_user(date)
    created_demand_user=get_created_demand_user(date)

    list1=[item for item in login_user_list if item not in created_project_user and item not in created_demand_user]

    
    return list1


def get_sendmail_user_num(date):
    return ProjectTargetCompanyDetail.objects.filter(add_time__lt=date,add_time__gte=(date-aDay),is_delete=False).values('member_id').distinct().count()
