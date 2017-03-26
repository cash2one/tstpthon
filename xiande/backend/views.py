#-*-encoding:utf-8-*-
from django.shortcuts import render, render_to_response, redirect, HttpResponse, RequestContext, get_object_or_404
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib import messages
from backend.decorators import backend_login_required, backend_staff_passes_test, backend_superuser_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from member.models import UserProfile,Income,Apply
from event.models import CashEventInfo,EventApply,BBBEventInfo,Event
import datetime
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from member.views import get_income,get_amount,get_month_amount,get_month_num

#Dashboard
@backend_login_required
@backend_staff_passes_test
def index(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))

#账户管理
@csrf_protect
def signin(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_url=request.GET.get('next',None)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect("backend.index")
            else:
                messages.warning(request, "您的帐号暂时不可用！")
        else:
            messages.warning(request, "您的帐号或密码输入错误！")

    return render_to_response("backend/signin.html", c, context_instance=RequestContext(request))


def signout(request):
    logout(request)
    return redirect("backend.signin")

@backend_login_required
@backend_staff_passes_test
def profile(request):

    c = {}
    c.update(csrf(request))
    isvalid = True
    

    if request.method == 'POST':


        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        new_password2 = request.POST['new_password2']
       
        if old_password.strip() =='':
            isvalid = False
            messages.warning(request, "请输入旧密码！")
        if new_password.strip() =='':
            isvalid = False
            messages.warning(request, "请输入新密码！")
        if new_password2.strip() =='':
            isvalid = False
            messages.warning(request, "请输入确认新密码！")
        if new_password.strip() != new_password2.strip():
            isvalid = False
            messages.warning(request, "两次输入新密码不同")

       
        if isvalid:
            try:
                username = request.user.username
            
                user = authenticate(username=username, password=old_password)
                if user is not None and user.is_active:

                    user.set_password(new_password)
                    user.save()            

                    messages.success(request,'密码修改成功！')
                else:
                    messages.warning(request,'旧密码错误！')
            except Exception, e:
                messages.warning(request,e.message)

    return render_to_response("backend/profile.html", context_instance=RequestContext(request))

@backend_login_required
@backend_staff_passes_test
def change_password(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))


#管理员管理
@backend_login_required
@backend_superuser_passes_test
def admin_list(request):
    c = {}
    c['user_list'] = User.objects.filter(is_staff=True).all()
   
    return render_to_response("backend/admin_list.html", c, context_instance=RequestContext(request))

@backend_login_required
@backend_superuser_passes_test
def admin_add(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))

@backend_login_required
@backend_superuser_passes_test
def admin_detail(request,id):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))

@backend_login_required
@backend_superuser_passes_test
def admin_edit(request,id):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))

@backend_login_required
@backend_superuser_passes_test
def admin_reset_password(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))

@csrf_exempt
@backend_login_required
@backend_superuser_passes_test
def admin_remove(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))


#用户管理
@backend_login_required
@backend_staff_passes_test
def user_list(request):
    c = {}
    c['item_list'] = UserProfile.objects.filter(is_investment=1,user__is_active=1).order_by('-id').all()
    return render_to_response("backend/user_list.html",c, context_instance=RequestContext(request))

@backend_login_required
@backend_staff_passes_test
def user_add(request):
    c = {}
    c.update(csrf(request))
    isvalid = True
    _user_info = UserProfile()

    if request.method == 'POST':

        username = request.POST['username']
        gender = request.POST['gender']
        is_investment = request.POST['is_investment']
        contract_no = request.POST['contract_no']
        fund_customer_number = request.POST['fund_customer_number']
        fund_item_number = request.POST['fund_item_number']
        amount = request.POST['amount']
        currency = request.POST['currency']
        borrowed_type = request.POST['borrowed_type']
        assign_type = request.POST['assign_type']
        id_type = request.POST['id_type']
        id_no = request.POST['id_no']
        birthday = request.POST['birthday']
        email = request.POST['email']
        address = request.POST['address']
        postcode = request.POST['postcode']
        contact = request.POST['contact']
        mobile = request.POST['mobile']
        tel = request.POST['tel']
        bank_name = request.POST['bank_name']
        bank_account = request.POST['bank_account']
        borrowed_time = request.POST['borrowed_time']
        borrowed_type = request.POST['borrowed_type']
        company = request.POST['company']
        job_title = request.POST['job_title']
        signed_time = request.POST['signed_time']
        contract_start_time = request.POST['contract_start_time']
        contract_end_time = request.POST['contract_end_time']
        family = request.POST['family']
        hobby = request.POST['hobby']
        memo = request.POST['memo']

        if username.strip() =='':
            isvalid = False
            messages.warning(request, "请输入用户名！")
        
        _user=User()
        max_id=User.objects.order_by('-id').first().id
        _user.username="XD"+str(max_id+1)
        _user.password=make_password(_user.username)
        _user.first_name=username
        _user.email=email

        _user_info.user=_user
        if gender !='':
            _user_info.gender=int(gender)
        if is_investment !='':
            _user_info.is_investment=int(is_investment)
        _user_info.contract_no=contract_no
        _user_info.fund_customer_number=fund_customer_number
        _user_info.fund_item_number=fund_item_number
        if currency !='':
            _user_info.currency=int(currency)
        if borrowed_type !='':
            _user_info.borrowed_type=int(borrowed_type)
        if id_type !='':
            _user_info.id_type=int(id_type)
        
        if assign_type !='':
            _user_info.assign_type=int(assign_type)

        _user_info.id_no=id_no
        if birthday !='':
            _user_info.birthday=datetime.datetime.strptime(birthday,'%m/%d/%Y')
        _user_info.address=address
        _user_info.postcode=postcode
        _user_info.contact=contact
        _user_info.mobile=mobile
        _user_info.tel=tel
        _user_info.bank_name=bank_name
        _user_info.bank_account=bank_account
        if borrowed_time !='':
            _user_info.borrowed_time=datetime.datetime.strptime(borrowed_time,'%m/%d/%Y')
        _user_info.company=company
        _user_info.job_title=job_title
        if signed_time !='':
            _user_info.signed_time=datetime.datetime.strptime(signed_time,'%m/%d/%Y')
        if contract_start_time !='':
            _user_info.contract_start_time=datetime.datetime.strptime(contract_start_time,'%m/%d/%Y')
        if contract_end_time !='':
            _user_info.contract_end_time=datetime.datetime.strptime(contract_end_time,'%m/%d/%Y')
        _user_info.family=family
        _user_info.hobby=hobby
        _user_info.memo=memo

        if amount!='':
            _user_info.amount=Decimal(amount)

        if isvalid:            
            _user.save()
            _user_info.user=_user
            _user_info.save()

            return redirect('backend.user_list')
    
    c['f']=_user_info
    return render_to_response("backend/user_edit.html",c, context_instance=RequestContext(request))


@backend_login_required
@backend_staff_passes_test
def user_edit(request,id):
    c = {}
    c.update(csrf(request))
    isvalid = True
    _user_info = get_object_or_404(UserProfile,pk=id)

    if request.method == 'POST':

        username = request.POST['username']
        gender = request.POST['gender']
        is_investment = request.POST['is_investment']
        contract_no = request.POST['contract_no']
        fund_customer_number = request.POST['fund_customer_number']
        fund_item_number = request.POST['fund_item_number']
        amount = request.POST['amount']
        currency = request.POST['currency']
        borrowed_type = request.POST['borrowed_type']
        assign_type = request.POST['assign_type']
        id_type = request.POST['id_type']
        id_no = request.POST['id_no']
        birthday = request.POST['birthday']
        email = request.POST['email']
        address = request.POST['address']
        postcode = request.POST['postcode']
        contact = request.POST['contact']
        mobile = request.POST['mobile']
        tel = request.POST['tel']
        bank_name = request.POST['bank_name']
        bank_account = request.POST['bank_account']
        borrowed_time = request.POST['borrowed_time']
        borrowed_type = request.POST['borrowed_type']
        company = request.POST['company']
        job_title = request.POST['job_title']
        signed_time = request.POST['signed_time']
        contract_start_time = request.POST['contract_start_time']
        contract_end_time = request.POST['contract_end_time']
        family = request.POST['family']
        hobby = request.POST['hobby']
        memo = request.POST['memo']

        if username.strip() =='':
            isvalid = False
            messages.warning(request, "请输入用户名！")
        
        _user_info.user.first_name=username
        _user_info.user.email=email

        if gender !='':
            _user_info.gender=int(gender)
        if is_investment !='':
            _user_info.is_investment=int(is_investment)

        _user_info.contract_no=contract_no
        _user_info.fund_customer_number=fund_customer_number
        _user_info.fund_item_number=fund_item_number
        if currency !='':
            _user_info.currency=int(currency)
        if borrowed_type !='':
            _user_info.borrowed_type=int(borrowed_type)
        if id_type !='':
            _user_info.id_type=int(id_type)
        if assign_type !='':
            _user_info.assign_type=int(assign_type)

        

        _user_info.id_no=id_no
        if birthday !='':
            _user_info.birthday=datetime.datetime.strptime(birthday,'%m/%d/%Y')
        _user_info.address=address
        _user_info.postcode=postcode
        _user_info.contact=contact
        _user_info.mobile=mobile
        _user_info.tel=tel
        _user_info.bank_name=bank_name
        _user_info.bank_account=bank_account

        if borrowed_time !='':
            _user_info.borrowed_time=datetime.datetime.strptime(borrowed_time,'%m/%d/%Y')
        _user_info.company=company
        _user_info.job_title=job_title
        if signed_time !='':
            _user_info.signed_time=datetime.datetime.strptime(signed_time,'%m/%d/%Y')
        if contract_start_time !='':
            _user_info.contract_start_time=datetime.datetime.strptime(contract_start_time,'%m/%d/%Y')
        if contract_end_time !='':
            _user_info.contract_end_time=datetime.datetime.strptime(contract_end_time,'%m/%d/%Y')
        _user_info.family=family
        _user_info.hobby=hobby
        _user_info.memo=memo

        if amount!='':
            _user_info.amount=Decimal(amount)

        if isvalid:            
            _user_info.user.save()

            _user_info.save()

            return redirect('backend.user_list')
    
    c['f']=_user_info
    return render_to_response("backend/user_edit.html",c, context_instance=RequestContext(request))

@backend_login_required
@backend_staff_passes_test
def user_reset_password(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))

@csrf_exempt
@backend_login_required
@backend_staff_passes_test
def user_remove(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            user_info =UserProfile.objects.get(pk=id)
            user=User.objects.get(pk=user_info.user.id)
            user.is_active=False
            user.save()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)

@backend_login_required
@backend_staff_passes_test
def apply_list(request):
    c = {}
    c['item_list'] = Apply.objects.exclude(status=3).all()
    return render_to_response("backend/apply_list.html",c, context_instance=RequestContext(request))

@csrf_exempt
@backend_login_required
@backend_staff_passes_test
def apply_remove(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            _apply =Apply.objects.get(pk=id)
            _apply.status=3
            _apply.save()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)

@csrf_exempt
@backend_login_required
@backend_staff_passes_test
def apply_approved(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            _apply =Apply.objects.get(pk=id)
            _apply.status=1
            _apply.save()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)

@csrf_exempt
@backend_login_required
@backend_staff_passes_test
def apply_disapproved(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            _apply =Apply.objects.get(pk=id)
            _apply.status=2
            _apply.save()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


@backend_login_required
@backend_staff_passes_test
def income_list(request):
    c = {}
    c['item_list'] = Income.objects.filter(is_active=True).all()
    return render_to_response("backend/income_list.html",c, context_instance=RequestContext(request))

@backend_login_required
@backend_staff_passes_test
def income_edit(request,id):
    c = {}
    c.update(csrf(request))
    isvalid = True
    income_item = get_object_or_404(Income,pk=id)

    if request.method == 'POST':


        amount = request.POST['amount']
        income = request.POST['income']
        
        assign_time = request.POST['assign_time']

        
        if amount.strip() =='':
            isvalid = False
            messages.warning(request, "请输入总本金！")
        if income.strip() =='':
            isvalid = False
            messages.warning(request, "请输入总收益！")
        
        if assign_time.strip() =='':
            isvalid = False
            messages.warning(request, "请输入结算日期！")

        income_item.amount=Decimal(amount)
        income_item.income=Decimal(income)
        income_item.assign_time=datetime.datetime.strptime(assign_time,'%m/%d/%Y')

        if isvalid:            
            
            income_item.save()

            return redirect('backend.income_list')
    
    c['f']=income_item

    return render_to_response("backend/income_edit.html",c, context_instance=RequestContext(request))




@backend_login_required
@backend_staff_passes_test
def income_add(request):
    c = {}
    c.update(csrf(request))
    isvalid = True
    income_item = Income()

    if request.method == 'POST':


        amount = request.POST['amount']
        income = request.POST['income']
        assign_time = request.POST['assign_time']

        
        if amount.strip() =='':
            isvalid = False
            messages.warning(request, "请输入总本金！")
        if income.strip() =='':
            isvalid = False
            messages.warning(request, "请输入总收益！")
        if assign_time.strip() =='':
            isvalid = False
            messages.warning(request, "请输入结算月份！")

        income_item.amount=Decimal(amount)
        income_item.income=Decimal(income)
        income_item.assign_time=datetime.datetime.strptime(assign_time,'%Y-%m')

        if isvalid:            
            
            income_item.save()

            return redirect('backend.income_list')
    
    c['f']=income_item

    return render_to_response("backend/income_edit.html",c, context_instance=RequestContext(request))




@csrf_exempt
@backend_login_required
@backend_staff_passes_test
def income_remove(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            income =Income.objects.get(pk=id)
            income.is_active=False
            income.save()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


#活动管理
@backend_login_required
@backend_staff_passes_test
def event_apply_list(request):
    c = {}
    c['item_list'] = EventApply.objects.exclude(status=3).all()
    return render_to_response("backend/event_apply_list.html",c, context_instance=RequestContext(request))

@csrf_exempt
@backend_login_required
@backend_staff_passes_test
def event_apply_remove(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            event_info =EventApply.objects.get(pk=id)
            event_info.status=3
            event_info.save()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)

@csrf_exempt
@backend_login_required
@backend_staff_passes_test
def event_apply_approved(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            event_info =EventApply.objects.get(pk=id)
            event_info.status=1
            event_info.save()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


@csrf_exempt
@backend_login_required
@backend_staff_passes_test
def event_apply_disapproved(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            event_info =EventApply.objects.get(pk=id)
            event_info.status=1
            event_info.save()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)


@backend_login_required
@backend_staff_passes_test
def event_user_list(request):
    c = {}
    c['item_list'] = UserProfile.objects.filter(is_investment=0,user__is_active=1).order_by('-id').all()
    return render_to_response("backend/event_user_list.html",c, context_instance=RequestContext(request))



@backend_login_required
@backend_staff_passes_test
def event_user_edit(request,id):
    c = {}
    c.update(csrf(request))
    isvalid = True
    _user_info = get_object_or_404(UserProfile,pk=id)

    if request.method == 'POST':

        username = request.POST['username']
        gender = request.POST['gender']
        is_investment = request.POST['is_investment']
        contract_no = request.POST['contract_no']
        fund_customer_number = request.POST['fund_customer_number']
        fund_item_number = request.POST['fund_item_number']
        amount = request.POST['amount']
        currency = request.POST['currency']
        borrowed_type = request.POST['borrowed_type']
        id_type = request.POST['id_type']
        id_no = request.POST['id_no']
        birthday = request.POST['birthday']
        email = request.POST['email']
        address = request.POST['address']
        postcode = request.POST['postcode']
        contact = request.POST['contact']
        mobile = request.POST['mobile']
        tel = request.POST['tel']
        bank_name = request.POST['bank_name']
        bank_account = request.POST['bank_account']
        borrowed_time = request.POST['borrowed_time']
        borrowed_type = request.POST['borrowed_type']
        company = request.POST['company']
        job_title = request.POST['job_title']
        signed_time = request.POST['signed_time']
        contract_start_time = request.POST['contract_start_time']
        contract_end_time = request.POST['contract_end_time']
        family = request.POST['family']
        hobby = request.POST['hobby']
        memo = request.POST['memo']

        if username.strip() =='':
            isvalid = False
            messages.warning(request, "请输入用户名！")
        
        _user_info.user.first_name=username
        _user_info.user.email=email

        if gender !='':
            _user_info.gender=int(gender)
        if is_investment !='':
            _user_info.is_investment=int(is_investment)

        _user_info.contract_no=contract_no
        _user_info.fund_customer_number=fund_customer_number
        _user_info.fund_item_number=fund_item_number
        if currency !='':
            _user_info.currency=int(currency)
        if borrowed_type !='':
            _user_info.borrowed_type=int(borrowed_type)
        if id_type !='':
            _user_info.id_type=int(id_type)
        _user_info.id_no=id_no
        if birthday !='':
            _user_info.birthday=datetime.datetime.strptime(birthday,'%m/%d/%Y')
        _user_info.address=address
        _user_info.postcode=postcode
        _user_info.contact=contact
        _user_info.mobile=mobile
        _user_info.tel=tel
        _user_info.bank_name=bank_name
        _user_info.bank_account=bank_account
        if borrowed_time !='':
            _user_info.borrowed_time=datetime.datetime.strptime(borrowed_time,'%m/%d/%Y')
        _user_info.company=company
        _user_info.job_title=job_title
        if signed_time !='':
            _user_info.signed_time=datetime.datetime.strptime(signed_time,'%m/%d/%Y')
        if contract_start_time !='':
            _user_info.contract_start_time=datetime.datetime.strptime(contract_start_time,'%m/%d/%Y')
        if contract_end_time !='':
            _user_info.contract_end_time=datetime.datetime.strptime(contract_end_time,'%m/%d/%Y')
        _user_info.family=family
        _user_info.hobby=hobby
        _user_info.memo=memo

        if amount!='':
            _user_info.amount=Decimal(amount)

        if isvalid:            
            _user_info.user.save()

            _user_info.save()

            return redirect('backend.event_user_list')
    
    c['f']=_user_info
    return render_to_response("backend/user_edit.html",c, context_instance=RequestContext(request))


@csrf_exempt
@backend_login_required
@backend_staff_passes_test
def event_user_remove(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            user_info =UserProfile.objects.get(pk=id)
            user=User.objects.get(pk=user_info.user.id)
            user.is_active=False
            user.save()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)

#小金库活动管理
@backend_login_required
@backend_staff_passes_test
def money_apply_list(request):
    c = {}
    _item_list = CashEventInfo.objects.exclude(status=3).all()
    for item in _item_list:
        if UserProfile.objects.exclude(wx_openid='').filter(wx_openid=item.introducer).count()>0:
            item.introducer_name= UserProfile.objects.exclude(wx_openid='').filter(wx_openid=item.introducer).first().user.first_name

    c['item_list'] = _item_list
    return render_to_response("backend/money_apply_list.html",c, context_instance=RequestContext(request))

@csrf_exempt
@backend_login_required
@backend_staff_passes_test
def money_apply_remove(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            cash_info =CashEventInfo.objects.get(pk=id)
            cash_info.status=3
            cash_info.save()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)

@csrf_exempt
@backend_login_required
@backend_staff_passes_test
def money_apply_disapproved(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            cash_info =CashEventInfo.objects.get(pk=id)
            cash_info.status=2
            cash_info.save()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)




@backend_login_required
@backend_staff_passes_test
def money_apply_approved(request,id):
    c = {}
    c.update(csrf(request))
    isvalid = True
    apply_item = get_object_or_404(CashEventInfo,pk=id)

    if request.method == 'POST':
        event_amount = request.POST['event_amount']
        
        if event_amount.strip() =='':
            isvalid = False
            messages.warning(request, "请输入金额！")

        if isvalid:            
            apply_item.event_amount=Decimal(event_amount)
            apply_item.event_add_time=datetime.datetime.now()
            apply_item.status=1
            apply_item.save()

            return redirect('backend.money_user_list')
    c['f']=apply_item
    return render_to_response("backend/money_apply_approved.html",c, context_instance=RequestContext(request))



@backend_login_required
@backend_staff_passes_test
def money_user_list(request):
    c = {}
    _item_list = CashEventInfo.objects.filter(status=1).all()

    for item in _item_list:
        item.event_all_amount=get_amount(item.user)
        item.event_all_income=get_income(item.user)
        item.event_recommond_amount=get_month_amount(item.user)
        item.event_recommond_num=get_month_num(item.user)

        if UserProfile.objects.exclude(wx_openid='').filter(wx_openid=item.introducer).count()>0:
            item.introducer_name= UserProfile.objects.exclude(wx_openid='').filter(wx_openid=item.introducer).first().user.first_name

    c['item_list'] = _item_list
    return render_to_response("backend/money_user_list.html",c, context_instance=RequestContext(request))

@backend_login_required
@backend_staff_passes_test
def money_user_edit(request,id):
    pass

@csrf_exempt
@backend_login_required
@backend_staff_passes_test
def money_user_remove(request):
    msg = ""
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            user_info =UserProfile.objects.get(pk=id)
            user=User.objects.get(pk=user_info.user.id)
            user.is_active=False
            user.save()
            msg = "success"
        except Exception, e:
            msg = e.message
    return HttpResponse(msg)



@backend_login_required
@backend_staff_passes_test
def bbb(request):
    c = {}
    c.update(csrf(request))
    isvalid = True

    _event = get_object_or_404(Event,code='BBB')
    _item_list = BBBEventInfo.objects.exclude(apply_status=3).order_by('-id')

    for item in _item_list:
        if BBBEventInfo.objects.exclude(openid='').filter(openid=item.introducer).count()>0:
            item.introducer_name= BBBEventInfo.objects.exclude(openid='').filter(openid=item.introducer).first().username

    c['item_list'] = _item_list

    if request.method == 'POST':

        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
       
        
        if start_time.strip() =='':
            isvalid = False
            messages.warning(request, "请输入开始时间！")
        if end_time.strip() =='':
            isvalid = False
            messages.warning(request, "请输入结束时间！")
        
       
        if start_time.strip() !='':
            _event.start_time=datetime.datetime.strptime(start_time,'%m/%d/%Y')
        if end_time.strip() !='':
            _event.end_time=datetime.datetime.strptime(end_time,'%m/%d/%Y')
        
        if _event.start_time >= _event.end_time :
            isvalid = False
            messages.warning(request, "结束时间必须大于开始时间！")

        if isvalid:                        
            _event.save()
            return redirect('backend.bbb')
    
    c['f']=_event
    return render_to_response("backend/bbb.html",c, context_instance=RequestContext(request))

