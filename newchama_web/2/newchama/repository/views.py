from django.shortcuts import render, HttpResponse, render_to_response, get_object_or_404, RequestContext, redirect
from repository.models import ListedCompany, AccountingFirm, Keyword, InvestmentCompany
from member.models import Member, Company
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from newchama.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import messages
# Create your views here.


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


def get_audit_companies(request, keyword):
    try:
        if keyword != "":
            audit_list = AccountingFirm.objects.filter(Q(name_en__icontains=keyword) | Q(name_cn__contains=keyword)
                                                       | Q(short_name_en__icontains=keyword) | Q(short_name_cn__contains=keyword))
            data = serializers.serialize('json', audit_list)
            return HttpResponse(data, mimetype='javascript/json')
        return None
    except ObjectDoesNotExist:
        return HttpResponse({"error", "error"}, mimetype='javascript/json')


def get_investment_companies(request, short_name_en):
    companies = InvestmentCompany.objects.filter(short_name_en__contains=short_name_en)[0:10]
    data = serializers.serialize('json', companies, fields=('short_name_cn', 'short_name_en', 'name_en'))
    return HttpResponse(data, mimetype='javascript/json')


def get_investment_company(request, id):
    try:
        company = InvestmentCompany.objects.filter(pk=id)[0:1]
        data = serializers.serialize('json', company)
        return HttpResponse(data, mimetype='javascript/json')
    except ObjectDoesNotExist:
        return None


def get_active_companies(request, keyword):
    try:
        if keyword != "":
            active_list = Company.objects.filter(Q(name_en__icontains=keyword) | Q(name_cn__contains=keyword) | Q(short_name_en__icontains=keyword) | Q(short_name_cn__contains=keyword), Q(status=0) | Q(status=1) | Q(status=4))[0: 10]
        data = serializers.serialize('json', active_list)
        return HttpResponse(data, mimetype='javascript/json')
    except ObjectDoesNotExist:
        return HttpResponse({"error", "error"}, mimetype='javascript/json')


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
        return HttpResponse(r)
    except Exception, e:
        return HttpResponse('[{"error":"'+e.message+'"}]')


@login_required
def keywords(request):
    keyword = request.GET.get("keyword", "")
    if keyword != "":
        result_list = Keyword.objects.filter(name__contains=keyword, is_delete=0).order_by("-count_project", "-id")
    else:
        result_list = Keyword.objects.filter(is_delete=0).order_by("-count_project", "-id")
    c = {}
    c["result_list"] = result_list
    c["keyword"] = keyword
    return render_to_response("repository/keywords.html", c, context_instance=RequestContext(request))


@login_required
@csrf_protect
def addKeyword(request):
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
        try:
            k = Keyword()
            k.name = request.POST.get("name", False)
            k.save()
            return redirect("repository.keywords")
        except Exception, e:
            messages.warning(request, e.message)
    c['k'] = Keyword
    return render_to_response("repository/add.html", c, context_instance=RequestContext(request))


@login_required
@csrf_protect
def editKeyword(request, id):
    c = {}
    c.update(csrf(request))
    k = get_object_or_404(Keyword, pk=id)
    if request.method == "POST":
        try:
            id_post = request.POST["id"]
            k = Keyword.objects.get(pk=id_post)
            k.name = request.POST.get("name", False)
            k.save()
            return redirect("repository.keywords")
        except Exception, e:
            messages.warning(request, e.message)
    c['k'] = k
    return render_to_response("repository/edit.html", c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def removeKeyword(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            Keyword.objects.filter(pk=id).update(is_delete=1)
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


@csrf_exempt
@login_required
def get_active_member(request, keyword):
    try:
        if keyword != "":
            active_list = Member.objects.filter(Q(first_name__icontains=keyword) | Q(last_name__contains=keyword), status=1)#.exclude(id=member_id)
        data = serializers.serialize('json', active_list)
        return HttpResponse(data, mimetype='javascript/json')
    except ObjectDoesNotExist:
        return HttpResponse({"error", "error"}, mimetype='javascript/json')
