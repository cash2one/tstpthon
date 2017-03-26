# -*- coding: utf-8 -*-  
from django.shortcuts import render, HttpResponse
from services.models import Province, Industry, City, AccountingFirm, ListedCompany, Keyword, Company, Member, InvestmentCompany
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from newchama.helper import member_login_required
from PIL import Image
import os
from newchama import settings
from django.utils.translation import ugettext_lazy as _, ugettext
import random
import uuid
# Create your views here.


def get_provinces(request, country_id):
    try:
        provinces = Province.objects.filter(country_id=country_id).order_by("-sort")
        data = serializers.serialize('json', provinces)
        return HttpResponse(data, mimetype='javascript/json')
    except ObjectDoesNotExist:
        return HttpResponse({"error", "error"}, mimetype='javascript/json')


def get_cities(request, province_id):
    cities = City.objects.filter(province_id=province_id)
    data = serializers.serialize('json', cities)
    return HttpResponse(data, mimetype='javascript/json')


def get_industrys(request, id):
    try:
        if id != "0":
            industry_list = Industry.objects.filter(father=id)
        else:
            industry_list = Industry.objects.filter(father__isnull=True)
        data = serializers.serialize('json', industry_list)
        return HttpResponse(data, mimetype='javascript/json')
    except ObjectDoesNotExist:
        return HttpResponse({"error", "error"}, mimetype='javascript/json')


def get_audit_companies(request, keyword):
    try:
        if keyword != "":
            audit_list = AccountingFirm.objects.filter(Q(name_en__icontains=keyword) | Q(name_cn__contains=keyword)
                                                       | Q(short_name_en__icontains=keyword) | Q(short_name_cn__contains=keyword))
        data = serializers.serialize('json', audit_list)
        return HttpResponse(data, mimetype='javascript/json')
    except ObjectDoesNotExist:
        return HttpResponse({"error", "error"}, mimetype='javascript/json')


def get_listed_companies(request, stock_symbol):
    companies = ListedCompany.objects.filter(stock_symbol__contains=stock_symbol)[0:10]
    data = serializers.serialize('json', companies, fields=('short_name_cn', 'short_name_en', 'stock_symbol'))
    return HttpResponse(data, mimetype='javascript/json')


def get_listed_company(request, id):
    try:
        company = ListedCompany.objects.filter(pk=id)[0:1]
        data = serializers.serialize('json', company)
        return HttpResponse(data, mimetype='javascript/json')
    except ObjectDoesNotExist:
        return None


def get_industry(request, id):
    try:
        industry = Industry.objects.get(pk=id)
        id = industry.id
        level = industry.level
        father_id = industry.father_id
        father_father_id = industry.father.father_id
        if father_id is None:
            father_id = 0
        if father_father_id is None:
            father_father_id = 0
        data = '{"id":%d,"level":%d ,"father_id":%d ,"father_father_id":%d}' % (id, level, father_id, father_father_id)
        return HttpResponse(data, mimetype='javascript/json')
    except ObjectDoesNotExist:
        return None


@csrf_exempt
@member_login_required
def upload_message_file(request):
    path = settings.MEDIA_ROOT + "/temp/"
    try:
        uploadfile = request.FILES.get("uploadFile")
        if uploadfile.size > 50000000:
            return HttpResponse('{"status": "error", "message": " %s "}' % ugettext("The file cannot be more than 50M"))
        if not os.path.exists(path):
            os.makedirs(path)

        old_name = os.path.splitext(uploadfile.name)[0]+os.path.splitext(uploadfile.name)[1]
        file_ext = os.path.splitext(uploadfile.name)[1]
        ext_name=['.jpg','.png','.jpeg','.doc','.docx','.xls','.xlsx','.ppt','.pptx','.pdf']
        if file_ext.lower() in ext_name:
            
            file_name = str(uuid.uuid1()) + file_ext
            destination = open(path + file_name, 'wb+')
            for chunk in uploadfile.chunks():
                destination.write(chunk)
            destination.close()
            return HttpResponse('{"status": "success", "path": "' + settings.MEDIA_URL + "temp/" + file_name + '", "oldname": "' + old_name + '"}')
        else:
            return HttpResponse('{"status": "error", "message": " %s "}' % ugettext("Only Support JPG, JEPG, PNG, DOC,DOCX,XLS,XLSX,PPT,PPTX,PDF"))
    except Exception, e:
        return HttpResponse('{"status": "error", "message": "' + e.message + '"}')


@csrf_exempt
@member_login_required
def upload_file(request):
    path = settings.MEDIA_ROOT + "/temp/"
    try:
        uploadfile = request.FILES.get("uploadFile")
        if uploadfile.size > 500000:
            return HttpResponse('{"status": "error", "message": " %s "}' % ugettext("The file cannot be more than 500K"))
        if not os.path.exists(path):
            os.makedirs(path)
        file_ext = os.path.splitext(uploadfile.name)[1]
        if file_ext.lower() == ".jpg" or file_ext.lower() == ".png" or file_ext.lower() == ".jepg":
            img = Image.open(uploadfile).size
            imgWidth = str(img[0])
            imgHeight = str(img[1])
            file_name = str(uuid.uuid1()) + file_ext
            destination = open(path + file_name, 'wb+')
            for chunk in uploadfile.chunks():
                destination.write(chunk)
            destination.close()
            return HttpResponse('{"status": "success", "path": "' + settings.MEDIA_URL + "temp/" + file_name + '", "imgName": "' + file_name + '", "imgWidth": "' + imgWidth + '", "imgHeight": "' + imgHeight + '"}')
        else:
            return HttpResponse('{"status": "error", "message": " %s "}' % ugettext("Only Support JPG, JEPG, PNG"))
    except Exception, e:
        return HttpResponse('{"status": "error", "message": "' + e.message + '"}')


def getKeywords(request):
    try:
        keyword = request.GET.get("term", "")
        inTags = request.GET.get("inTags", "")
        r = "";
        if keyword != "":
            if inTags != "":
                its = inTags.split(",")
                data = Keyword.objects.filter(name__icontains=keyword, is_delete=0).exclude(name__in=its)[0:10]
            else:
                data = Keyword.objects.filter(name__icontains=keyword, is_delete=0)[0:10]
            if data:
                r = "["
                for k in data:
                    r += '{"id":"'+str(k.id)+'","label":"'+k.name+'","value":"'+k.name+'"},'
                r = r[0:len(r)-1] + "]"
            else:
                r = "[]"
        return HttpResponse(r)
    except Exception, e:
        return HttpResponse('[{"error":"'+e.message+'"}]')


def get_active_companies(request, keyword):
    try:
        if keyword != "":
            active_list = Company.objects.filter(Q(name_en__icontains=keyword) | Q(name_cn__contains=keyword) | Q(short_name_en__icontains=keyword) | Q(short_name_cn__contains=keyword), Q(status=0) | Q(status=1) | Q(status=4))[0: 10]
        data = serializers.serialize('json', active_list)
        return HttpResponse(data, mimetype='javascript/json')
    except ObjectDoesNotExist:
        return HttpResponse({"error", "error"}, mimetype='javascript/json')


def get_companies(request, keyword):
    try:
        if keyword != "":
            active_list = Company.objects.filter(Q(name_en__icontains=keyword) | Q(name_cn__contains=keyword) | Q(short_name_en__icontains=keyword) | Q(short_name_cn__contains=keyword)).exclude(id=27)[0: 10]
        data = serializers.serialize('json', active_list)
        return HttpResponse(data, mimetype='javascript/json')
    except ObjectDoesNotExist:
        return HttpResponse({"error", "error"}, mimetype='javascript/json')


def get_active_company(request, id):
    try:
        company = Company.objects.filter(pk=id)[0:1]
        data = serializers.serialize('json', company)
        return HttpResponse(data, mimetype='javascript/json')
    except ObjectDoesNotExist:
        return None


def get_investment_companies(request, keyword):
    try:
        if keyword != "":
            # company_id = request.session['member']['company_id']
            active_list = InvestmentCompany.objects.filter(Q(name_en__icontains=keyword) | Q(name_cn__contains=keyword) | Q(short_name_en__icontains=keyword) | Q(short_name_cn__contains=keyword)).order_by("-found_time")[0: 10]
        data = serializers.serialize('json', active_list)
        return HttpResponse(data, mimetype='javascript/json')
    except Exception, e:
        return HttpResponse('[{"error":"'+e.message+'"}]')


def get_active_member(request, keyword):
    try:
        if keyword != "":
            member_id = request.session['member']['id']
            active_list = Member.objects.filter(Q(first_name__icontains=keyword) | Q(last_name__contains=keyword), status=1).exclude(id=member_id)
        data = serializers.serialize('json', active_list)
        return HttpResponse(data, mimetype='javascript/json')
    except ObjectDoesNotExist:
        return HttpResponse({"error", "error"}, mimetype='javascript/json')



def convert_finance_type_to_num(finance_type):

    if finance_type==99:
        num_min = 0
        num_max = 99999999999999
    elif finance_type==1:
        num_min = 0
        num_max = 10*10000000
    elif finance_type==2:
        num_min = 10*10000000
        num_max = 20*10000000
    elif finance_type==3:
        num_min = 20*10000000
        num_max = 50*10000000
    elif finance_type==4:
        num_min = 50*10000000
        num_max = 100*10000000
    elif finance_type==5:
        num_min = 100*10000000
        num_max = 200*10000000
    elif finance_type==6:
        num_min = 200*10000000
        num_max = 300*10000000
    elif finance_type==7:
        num_min = 300*10000000
        num_max = 500*10000000
    elif finance_type==8:
        num_min = 500*10000000
        num_max = 1000*10000000
    elif finance_type==9:
        num_min = 1000*10000000
        num_max = 2000*10000000
    elif finance_type==10:
        num_min = 2000*10000000
        num_max = 3000*10000000
    elif finance_type==11:
        num_min = 3000*10000000
        num_max = 99999999999999
    else:
        num_min=0
        num_max=0

    return num_min,num_max


def convert_growth_type_to_num(finance_type):

    if finance_type==99:
        num_min = 0
        num_max = 99999999999999
    elif finance_type==1:
        num_min = 0
        num_max = 10
    elif finance_type==2:
        num_min = 10
        num_max = 30
    elif finance_type==3:
        num_min = 30
        num_max = 50
    elif finance_type==4:
        num_min = 50
        num_max = 70
    elif finance_type==5:
        num_min = 70
        num_max = 100
    elif finance_type==6:
        num_min = 100
        num_max = 150

    elif finance_type==7:
        num_min = 150
        num_max = 99999999999999
    else:
        num_min=0
        num_max=0

    return num_min,num_max

