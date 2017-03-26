#-*-encoding:utf-8-*-
import datetime
from django.shortcuts import render
from log.models import AdminLog


def GetRemoteIpAddress(request):
    ip=""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_write(request,user,operation_type,target_type,detail_type,item_id,item_name,memo):
    _log = AdminLog()
    _log.user=user
    _log.operation_type=operation_type
    _log.target_type=target_type
    _log.detail_type=detail_type
    _log.item_id=item_id
    _log.item_name=item_name
    _log.ip=GetRemoteIpAddress(request)
    _log.request_url=request.get_full_path()
    _log.memo=memo
    _log.save()
    return _log.id



def write_search_project_log(request,user,memo):
    log_write(request,user,9,2,0,user.id,user.first_name,memo)

def write_search_demand_log(request,user,memo):
    log_write(request,user,9,3,0,user.id,user.first_name,memo)

def write_search_news_log(request,user,memo):
    log_write(request,user,9,6,0,user.id,user.first_name,memo)

def write_login_log(request,user,memo):
    log_write(request,user,1,1,0,user.id,user.first_name,memo)

def write_member_view_log(request,user,item):
    log_write(request,user,2,1,0,item.id,item.first_name,'')

def write_company_view_log(request,user,item,memo):
    log_write(request,user,2,4,0,item.id,item.name_cn,memo)


def write_company_view_recommond_man_log(request,user,item,memo):
    log_write(request,user,2,5,5,item.id,item.name_cn,memo)


def write_company_view_recommond_machine_log(request,user,item,memo):
    log_write(request,user,2,5,6,item.id,item.name_cn,memo)


def write_project_view_log(request,user,item):
    save_dynamic(user, 2, item.id, item.name_cn)
    log_write(request,user,2,2,1,item.id,item.name_cn,'')


def write_project_teaser_view_log(request,user,item):
    log_write(request,user,2,2,2,item.id,item.name_cn,'')

def write_demand_view_log(request,user,item):
    save_dynamic(user, 3, item.id, item.name_cn)
    log_write(request,user,2,3,1,item.id,item.name_cn,'')


def write_demand_teaser_view_log(request,user,item):
    log_write(request,user,2,3,2,item.id,item.name_cn,'')


def write_project_edit_log(request,user,item):
    log_write(request,user,3,2,0,item.id,item.name_cn,'')

def write_demand_edit_log(request,user,item):
    log_write(request,user,3,3,0,item.id,item.name_cn,'')


def write_project_offline_log(request,user,item):
    log_write(request,user,4,2,0,item.id,item.name_cn,'')

def write_demand_offline_log(request,user,item):
    log_write(request,user,4,3,0,item.id,item.name_cn,'')


def write_project_pending_log(request,user,item):
    log_write(request,user,10,2,0,item.id,item.name_cn,'')


def write_demand_pending_log(request,user,item):
    log_write(request,user,10,3,0,item.id,item.name_cn,'')


def write_project_delete_log(request,user,item):
    log_write(request,user,7,2,0,item.id,item.name_cn,'')

def write_demand_delete_log(request,user,item):
    log_write(request,user,7,3,0,item.id,item.name_cn,'')


def write_project_favorite_log(request,user,item):
    log_write(request,user,5,2,0,item.id,item.name_cn,'')

def write_demand_favorite_log(request,user,item):
    log_write(request,user,5,3,0,item.id,item.name_cn,'')

def write_member_favorite_log(request,user,item):
    log_write(request,user,5,1,0,item.id,item.first_name + ' ' + item.last_name,'')

def write_company_favorite_log(request,user,item):
    log_write(request,user,5,4,0,item.id,item.name_cn,'')

def write_news_favorite_log(request,user,item):
    log_write(request,user,5,6,0,item.id,item.title,'')

def write_project_remove_favorite_log(request,user,item):
    log_write(request,user,6,2,0,item.id,item.name_cn,'')

def write_demand_remove_favorite_log(request,user,item):
    log_write(request,user,6,3,0,item.id,item.name_cn,'')

def write_member_remove_favorite_log(request,user,item):
    log_write(request,user,6,1,0,item.id,item.first_name + ' ' + item.last_name,'')

def write_company_remove_favorite_log(request,user,item):
    log_write(request,user,6,4,0,item.id,item.name_cn,'')

def write_news_remove_favorite_log(request,user,item):
    log_write(request,user,6,6,0,item.id,item.title,'')

def write_extenal_mail_log(request,user,item,email_list):
    for email in email_list:
        log_write(request,user,0,7,0,item.id,item.name_cn,email)

def write_view_index_log(request, user, memo):
    log_write(request, user, 2, 8, 0, user.id, user.first_name, memo)

def write_email_log(request, user, item):
    log_write(request, user, 2, 9, item["type"], item["id"], item["title"], item["date"])
