from django.shortcuts import render,render_to_response, redirect
from newchama.settings import LANGUAGE_COOKIE_NAME,NUM
from services.models import AccountingFirm, ListedCompany, StockExchange, Project, Country, Province, Company, Member, StockStructure, Industry, StatusProject, Message, ProjectViewLog, ProjectServiceType, City, ProjectKeyword,CompanyWithPE,IndustryWithPE
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.template import RequestContext
from services.models import Member, EntryForm
from django.contrib import messages
from django.utils.translation import ugettext, ugettext_lazy as _
# Create your views here.


def baidu_verify_hDP2Pd8fky(request):
    return render_to_response("home/"+request.lang+"/baidu_verify_hDP2Pd8fky.html")

def index(request):
    if request.session.get('member', False):
        return redirect("account.index")
    else:
        response = render_to_response("home/"+request.lang+"/index_new.html")
        return response
	# response = render_to_response("home/"+request.lang+"/index_new.html")
	# return response

def products(request):
    response = render_to_response("home/"+request.lang+"/products.html")
    response.set_cookie(LANGUAGE_COOKIE_NAME,request.lang)
    return response

def us(request):
    response = render_to_response("home/"+request.lang+"/us.html")
    response.set_cookie(LANGUAGE_COOKIE_NAME,request.lang)
    return response


def bd(request):
    response = render_to_response("home/"+request.lang+"/bd.html")
    response.set_cookie(LANGUAGE_COOKIE_NAME,request.lang)
    return response


def contact(request):
    response = render_to_response("home/"+request.lang+"/contact.html")
    response.set_cookie(LANGUAGE_COOKIE_NAME,request.lang)
    return response

def m_step1(request):
    response = render_to_response("home/"+request.lang+"/m_step1.html")
    response.set_cookie(LANGUAGE_COOKIE_NAME,request.lang)
    return response

def m_step2(request):
    c = {}
    c.update(csrf(request))
    isvalid = True
    form = EntryForm()

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        mobile = request.POST['mobile']
        username = request.POST['username']
        company_name = request.POST['company_name']
        company_type = request.POST.get('company_type', "")

        

        if email.strip() == "":
            isvalid = False
            messages.warning(request, _("please input your email"))
        if password.strip() == "":
            isvalid = False
            messages.warning(request, _("please input your password"))
        
        if company_type == "":
            isvalid = False
            messages.warning(request, _("please select your company type"))
        if company_name.strip() == "":
            isvalid = False
            messages.warning(request, _("please input your company"))
        
        if mobile.strip() == "":
            isvalid = False
            messages.warning(request, _("please input your mobile"))
        
        form.email = email
        form.fullname = username
        
        form.mobile = mobile
        
        form.company = company_name
        form.company_type = company_type
        
        if isvalid:
            is_exist = False
            count_email = Member.objects.filter(email=email).count()
            if count_email > 0:
                is_exist = True
                messages.warning(request, _("the email is existed"))
            count_mobile = Member.objects.filter(mobile=mobile).count()
            if count_mobile > 0:
                is_exist = True
                messages.warning(request, _("the mobile is existed"))
            if is_exist is False:
                form.make_password(password)
                form.save()
                return redirect('home.m_step3')

        
    c['f'] = form
    response = render_to_response("home/"+request.lang+"/m_step2.html", c, context_instance=RequestContext(request))

    response.set_cookie(LANGUAGE_COOKIE_NAME,request.lang)
    return response

def m_step3(request):
    response = render_to_response("home/"+request.lang+"/m_step3.html")
    response.set_cookie(LANGUAGE_COOKIE_NAME,request.lang)
    return response

def m_privacy(request):
    response = render_to_response("home/"+request.lang+"/m_privacy.html")
    response.set_cookie(LANGUAGE_COOKIE_NAME,request.lang)
    return response

def m_user(request):
    response = render_to_response("home/"+request.lang+"/m_user.html")
    response.set_cookie(LANGUAGE_COOKIE_NAME,request.lang)
    return response

def m_user(request):
    response = render_to_response("home/"+request.lang+"/m_user.html")
    response.set_cookie(LANGUAGE_COOKIE_NAME,request.lang)
    return response

def m_tag_index(request):
    response = render_to_response("home/"+request.lang+"/m_tag_index.html")
    response.set_cookie(LANGUAGE_COOKIE_NAME,request.lang)
    return response

def m_tag_list(request,id):
    c={}
    c['id']=id
    response = render_to_response("home/"+request.lang+"/m_tag_list.html",c, context_instance=RequestContext(request))
    response.set_cookie(LANGUAGE_COOKIE_NAME,request.lang)
    return response

