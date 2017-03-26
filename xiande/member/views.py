#-*-encoding:utf-8-*-
from django.shortcuts import render,render_to_response, redirect, HttpResponse, RequestContext, get_object_or_404
from member.models import Apply,UserProfile,Income
from event.models import CashEventInfo,CashEventRecommondInfo
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import datetime
from decimal import Decimal
from olive.settings import TIME_ZONE
from weixin.oauth import getJsApiTicket
from weixin.sign import Sign
from weixin.views import WEIXIN_TOKEN,APPID,APPSECRET
from wechat_sdk import WechatBasic

def index(request):
    c = {}
    openid = request.session.get("openid", "")
    if openid == "":
        return redirect("/oauth/?refer=/member/")
    
    user_num= UserProfile.objects.filter(wx_openid=openid).count()
    if user_num>0:
        _user_profile=UserProfile.objects.filter(wx_openid=openid).first()
        c['u']=_user_profile
    else:
        return redirect('member.first')

    return render_to_response("member/index.html",c, context_instance=RequestContext(request))


def money(request):
    c = {}
    openid = request.session.get("openid", "")
    if openid == "":
        return redirect("/oauth/?refer=/member/money/")

    has_cash=False
    user_num= UserProfile.objects.filter(wx_openid=openid).count()
    if user_num>0:
        _user_profile=UserProfile.objects.filter(wx_openid=openid).first()
        _cash_record_num = CashEventInfo.objects.filter(user=_user_profile.user,status=1).count()
        if _cash_record_num>0:
            _cash_record =CashEventInfo.objects.filter(user=_user_profile.user,status=1).first()
            c['event_amount']=get_amount(_user_profile.user)
            c['recommond_amount']=get_month_amount(_user_profile.user)
            c['recommond_num']=get_month_num(_user_profile.user)
            c['income']=get_income(_user_profile.user)
            c['yesterday_income']=get_yesterday_income(_user_profile.user)

            c['all_amount']=float(c['event_amount'])+c['income']
            has_cash=True
            

        
    c['has_cash']=has_cash
    c['openid']=openid

    wechat = WechatBasic(token=WEIXIN_TOKEN,appid=APPID,appsecret=APPSECRET)
    ticket=getJsApiTicket(wechat)
    sign = Sign(ticket,"http://"+request.get_host()+request.get_full_path())
    c['sign']=sign.sign()
    c['appid']=APPID
    c['openid']=openid

    return render_to_response("member/money.html", c,context_instance=RequestContext(request))

def get_yesterday_income(user):
    _num=0
    _cash_record_num = CashEventInfo.objects.filter(user=user,status=1).count()
    if _cash_record_num>0:
        _cash_record =CashEventInfo.objects.filter(user=user,status=1).first()

        _days=(datetime.datetime.today()-_cash_record.event_add_time.replace(tzinfo=None)).days
        if _days>0:
            rate=1*0.12/365
            _num+=round(float(_cash_record.event_amount)*rate,2)
    
    _cash_recommond_record_list=CashEventRecommondInfo.objects.filter(introducer=user,add_time__lt=datetime.date.today().replace(day=1))

    for _record in _cash_recommond_record_list:
        next_day=(_record.add_time.replace(day=1) + datetime.timedelta(31)).replace(day=1).replace(tzinfo=None)

        _days=(datetime.datetime.today()-next_day).days
        if _days>0:
            rate=1*0.12/365
            _num+=round(float(_record.amount)*rate,2)

    return _num

def get_income(user):
    _num=0
    _cash_record_num = CashEventInfo.objects.filter(user=user,status=1).count()
    if _cash_record_num>0:
        _cash_record =CashEventInfo.objects.filter(user=user,status=1).first()

        _days=(datetime.datetime.today()-_cash_record.event_add_time.replace(tzinfo=None)).days
        if _days>0:
            rate=_days*0.12/365
            _num+=round(float(_cash_record.event_amount)*rate,2)
    
    _cash_recommond_record_list=CashEventRecommondInfo.objects.filter(introducer=user,add_time__lt=datetime.date.today().replace(day=1))

    for _record in _cash_recommond_record_list:
        next_day=(_record.add_time.replace(day=1) + datetime.timedelta(31)).replace(day=1).replace(tzinfo=None)

        _days=(datetime.datetime.today()-next_day).days
        if _days>0:
            rate=_days*0.12/365
            _num+=round(float(_record.amount)*rate,2)

    return _num

def get_amount(user):
    _num=0
    _cash_record_num = CashEventInfo.objects.filter(user=user,status=1).count()
    if _cash_record_num>0:
        _cash_record =CashEventInfo.objects.filter(user=user,status=1).first()
        _num+=_cash_record.event_amount

    _cash_recommond_record_list=CashEventRecommondInfo.objects.filter(introducer=user,add_time__lt=datetime.date.today().replace(day=1))

    for _record in _cash_recommond_record_list:
        _num+=_record.amount

    return _num


def get_month_amount(user):
    _num=0
    
    _cash_recommond_record_list=CashEventRecommondInfo.objects.filter(introducer=user,add_time__gte=datetime.date.today().replace(day=1))

    for _record in _cash_recommond_record_list:
        _num+=_record.amount

    return _num


def get_month_num(user):
    return CashEventRecommondInfo.objects.filter(introducer=user,add_time__gte=datetime.date.today().replace(day=1)).count()


def assets(request):
    c = {}
    openid = request.session.get("openid", "")
    if openid == "":
        return redirect("/oauth/?refer=/member/assets/")
    
    user_num= UserProfile.objects.filter(wx_openid=openid).count()
    if user_num>0:
        _user_profile=UserProfile.objects.filter(wx_openid=openid).first()
        if not _user_profile.is_investment:
            return redirect('member.index')
        c['u']=_user_profile
        _income=Income.objects.filter(is_active=True).order_by('-assign_time').first()
        c['income']=100*_income.income/_income.amount
    else:
        return redirect('member.first')

    return render_to_response("member/assets.html",c, context_instance=RequestContext(request))


def logout(request):
    openid = request.session.get("openid", "")
    if openid == "":
        return redirect("/oauth/?refer=/member/logout")

    openid_member_num = UserProfile.objects.filter(wx_openid=openid).count()

    if  openid_member_num>0:
        user_profile = UserProfile.objects.filter(wx_openid=openid).first()

        user_profile.wx_openid=''
        user_profile.save()

    return redirect("member.index")

def first(request):
    c = {}
    c.update(csrf(request))
    
    openid = request.session.get("openid", "")
    if openid == "":
        return redirect("/oauth/?refer=/member/first")

    isvalid = True
    f={}

    if request.method == 'POST':
        username = request.POST['username']
        mobile = request.POST['mobile']
        customer_number = request.POST['customer_number']
        idcard = request.POST['idcard']

        if username.strip() == "":
            isvalid = False
            messages.warning(request, "请输入姓名！")
        
        else:
            input_num=0
            if mobile.strip() != "":
                input_num+=1
        
            if customer_number.strip() != "":
                input_num+=1

            if idcard.strip() != "":
                input_num+=1
            
            if input_num <1:
                isvalid = False
                messages.warning(request, "请输入客户编号、身份证、手机中至少一项！")

        f['username'] = username
        f['mobile'] = mobile
        f['customer_number'] = customer_number
        f['idcard'] = idcard

        if isvalid:
            user_list=UserProfile.objects.exclude(user__is_active=0).filter(user__first_name=username).all()
            for user in user_list:

                if user.fund_customer_number==customer_number:
                    user.wx_openid=openid
                    user.save()
                    return redirect('member.index')
                if user.id_no==idcard:
                    user.wx_openid=openid
                    user.save()
                    return redirect('member.index')
                if user.mobile==mobile:
                    user.wx_openid=openid
                    user.save()
                    return redirect('member.index')
            
            messages.warning(request, "用户不存在，或您输入的资料有误，无法完成绑定，请及时您的联系客户经理！")
            
    c['f']=f
    return render_to_response("member/first.html", c, context_instance=RequestContext(request))




def join(request):
    c = {}
    c.update(csrf(request))

    isvalid = True
    isSuccess = False
    member_apply = Apply()

    f={}
    
    openid = request.session.get("openid", "")
    
    if openid == "":
        return redirect("/oauth/?refer=/member/join")
    
    
    openid_member_num = UserProfile.objects.filter(wx_openid=openid).count()

    if  openid_member_num>0:
        user_profile = UserProfile.objects.filter(wx_openid=openid).first()

        member_apply.user=user_profile.user
        f['username'] = user_profile.user.first_name
        f['mobile'] = user_profile.mobile
        f['address'] = user_profile.address
        f['idcard'] = user_profile.id_no
            
    

    if request.method == 'POST':
        username = request.POST['username']
        mobile = request.POST['mobile']
        address = request.POST['address']
        idcard = request.POST['idcard']

        amount=0
        if request.POST['amount'] !='' and request.POST['amount'].isdigit():
            amount = int(request.POST['amount'])

        project = int(request.POST['project'])

        if username.strip() == "":
            isvalid = False
            messages.warning(request, "请输入联系人！")
        if mobile.strip() == "":
            isvalid = False
            messages.warning(request, "请输入您的手机！")
        
        if address.strip() == "":
            isvalid = False
            messages.warning(request, "请输入您的地址！")

        if idcard.strip() == "":
            isvalid = False
            messages.warning(request, "请输入您的证件号码！")
        
        if amount == 0:
            isvalid = False
            messages.warning(request, "请输入您要理财的金额！")

        if project == 0:
            isvalid = False
            messages.warning(request, "请选择您要参加的项目！")
        

        f['username'] = username
        f['mobile'] = mobile
        f['address'] = address
        f['idcard'] = idcard
        f['amount']=amount
        f['project']=project


        if isvalid:
            user_num = UserProfile.objects.filter(user__first_name=username,mobile=mobile).count()
            if user_num >0:
                _user_profile=UserProfile.objects.filter(user__first_name=username,mobile=mobile).first()
                
                member_apply.user=_user_profile.user
            else:
                _user=User()
                max_id=User.objects.order_by('-id').first().id
                _user.username="XD"+str(max_id+1)
                _user.first_name=username
                _user.password=make_password(_user.username)
                _user.save()
                _new_user=User.objects.filter(username=_user.username).order_by('-id').first()
                
                _profile = UserProfile()
                _profile.user=_new_user
                _profile.mobile=mobile
                _profile.address=address
                _profile.id_no=idcard
                _profile.wx_openid=openid
                _profile.source=3
                _profile.save()
                member_apply.user=_new_user

            member_apply.amount=amount
            member_apply.project=project

            try:

                member_apply.save()
                isSuccess=True
                #messages.success(request, "您的理财申请已经提交成功！我们的客户经理会尽快与您联系！")

            except Exception, e:
                    messages.warning(request,e)
            

    c['f']= f
    c['is_ok'] = isSuccess
    return render_to_response("member/join.html", c, context_instance=RequestContext(request))
