#-*-encoding:utf-8-*-
from django.shortcuts import render,render_to_response, redirect, HttpResponse, RequestContext, get_object_or_404
from wechat_sdk import WechatBasic
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from event.models import EventApply,CashEventInfo,BBBEventInfo,Event,CashEventRecommondInfo
from member.models import UserProfile
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from weixin.oauth import getJsApiTicket
from weixin.sign import Sign
from weixin.views import WEIXIN_TOKEN,APPID,APPSECRET
import datetime
from decimal import Decimal
def bbb(request):
    c = {}
    c['introducer']=request.GET.get('u','')
    
    return render_to_response("event/bbb.html",c, context_instance=RequestContext(request))


def bbb_join(request):

    _event=get_object_or_404(Event,code='BBB')
    if _event.start_time.strftime("%Y-%m-%d") > datetime.datetime.now().strftime("%Y-%m-%d"):
        return redirect('event.bbb_wait')

    if _event.end_time.strftime("%Y-%m-%d") < datetime.datetime.now().strftime("%Y-%m-%d"):
        return redirect('event.bbb_end')

    c = {}
    c['introducer']=request.GET.get('u','')
    c.update(csrf(request))
    isvalid = True
    bbb_apply = BBBEventInfo()

    openid = request.session.get("openid", "")
    
    if openid == "":
        return redirect("/oauth/?refer=/event/bbb_join/?u="+c['introducer'])


    if request.method == 'POST':
        username = request.POST['username']
        mobile = request.POST['mobile']
        amount = request.POST['amount']

        if username.strip() == "":
            isvalid = False
            messages.warning(request, "请输入您的用户名！")
        if mobile.strip() == "":
            isvalid = False
            messages.warning(request, "请输入您的手机！")
        
        if amount == "":
            isvalid = False
            messages.warning(request, "请选择您要下注的金额！")
        
        bbb_apply.username=username
        bbb_apply.mobile=mobile
        bbb_apply.amount=amount
        bbb_apply.openid = openid
        bbb_apply.introducer= c['introducer']

        if isvalid:
            try:
                bbb_apply.save()
                return redirect('event.bbb_success')
            except Exception, e:
                messages.warning(request,e)

    c['f']=bbb_apply
    
    return render_to_response("event/bbb_join.html",c, context_instance=RequestContext(request))

def bbb_wait(request):
    c = {}
    openid = request.session.get("openid", "")
    
    if openid == "":
        return redirect("/oauth/?refer=/event/bbb_wait/")

    wechat = WechatBasic(token=WEIXIN_TOKEN,appid=APPID,appsecret=APPSECRET)
    ticket=getJsApiTicket(wechat)
    sign = Sign(ticket,"http://"+request.get_host()+request.get_full_path())
    c['sign']=sign.sign()
    c['appid']=APPID
    c['openid']=openid
    c['status']='wait'
    return render_to_response("event/bbb_success.html", c, context_instance=RequestContext(request))

def bbb_end(request):
    c = {}
    openid = request.session.get("openid", "")
    
    if openid == "":
        return redirect("/oauth/?refer=/event/bbb_end/")

    wechat = WechatBasic(token=WEIXIN_TOKEN,appid=APPID,appsecret=APPSECRET)
    ticket=getJsApiTicket(wechat)
    sign = Sign(ticket,"http://"+request.get_host()+request.get_full_path())
    c['sign']=sign.sign()
    c['appid']=APPID
    c['openid']=openid
    c['status']='end'
    return render_to_response("event/bbb_success.html", c, context_instance=RequestContext(request))


def bbb_success(request):
    c = {}
    openid = request.session.get("openid", "")
    
    if openid == "":
        return redirect("/oauth/?refer=/event/bbb_success/")

    wechat = WechatBasic(token=WEIXIN_TOKEN,appid=APPID,appsecret=APPSECRET)
    ticket=getJsApiTicket(wechat)
    sign = Sign(ticket,"http://"+request.get_host()+request.get_full_path())
    c['sign']=sign.sign()
    c['appid']=APPID
    c['openid']=openid
    c['status']='success'
    return render_to_response("event/bbb_success.html", c, context_instance=RequestContext(request))


def bbb_first(request):
    c = {}
    c['introducer']=request.GET.get('u','')
    openid = request.session.get("openid", "")
    
    if openid == "":
        return redirect("/oauth/?refer=/event/bbb_first/?u="+c['introducer'])


    wechat = WechatBasic(token=WEIXIN_TOKEN,appid=APPID,appsecret=APPSECRET)
    ticket=getJsApiTicket(wechat)
    sign = Sign(ticket,"http://"+request.get_host()+request.get_full_path())
    c['sign']=sign.sign()
    c['appid']=APPID
    c['openid']=openid
    return render_to_response("event/bbb_first.html", c, context_instance=RequestContext(request))




def cash(request):
    c = {}
    c['introducer']=request.GET.get('u','')
    openid = request.session.get("openid", '')
    if openid == "":
        return redirect("/oauth/?refer=/event/cash/?u="+c['introducer'])

    has_cash=False
    user_num= UserProfile.objects.filter(wx_openid=openid).count()
    if user_num>0:
        _user_profile=UserProfile.objects.filter(wx_openid=openid).first()
        _cash_record_num = CashEventInfo.objects.filter(user=_user_profile.user).count()
        if _cash_record_num>0:
            _cash_record =CashEventInfo.objects.filter(user=_user_profile.user).first()
            
            has_cash=True
            
        
    c['has_cash']=has_cash
    wechat = WechatBasic(token=WEIXIN_TOKEN,appid=APPID,appsecret=APPSECRET)
    ticket=getJsApiTicket(wechat)
    sign = Sign(ticket,"http://"+request.get_host()+request.get_full_path())
    c['sign']=sign.sign()
    c['appid']=APPID
    c['openid']=openid

    return render_to_response("event/cash.html",c, context_instance=RequestContext(request))

@csrf_protect
def cash_join(request):
    c = {}
    c.update(csrf(request))
    f={}
    isSuccess=False
    isvalid = True
    cash_event = CashEventInfo()
    c['introducer']=request.GET.get('u','')

    openid = request.session.get("openid", "")
    
    if openid == "":
        return redirect("/oauth/?refer=/event/cash_join/?u="+c['introducer'])

    openid_member_num = UserProfile.objects.filter(wx_openid=openid).count()

    if  openid_member_num>0:
        user_profile = UserProfile.objects.filter(wx_openid=openid).first()

        
        f['username'] = user_profile.user.first_name
        f['mobile'] = user_profile.mobile
        f['address'] = user_profile.address

        f['email']=user_profile.user.email
        f['company']=user_profile.company
        f['job_title']=user_profile.job_title
        f['fund_customer_number']=user_profile.fund_customer_number
        



    if request.method == 'POST':
        username = request.POST['username']
        mobile = request.POST['mobile']
        # address = request.POST['address']
        # email = request.POST['email']
        # company = request.POST['company']
        # job_title = request.POST['job_title']
        # hobby = request.POST['hobby']
        # household_spending = int(request.POST['household_spending'])
        # investment_apply = int(request.POST['investment_apply'])
        # investement_focus = int(request.POST['investement_focus'])
        # fund_customer_number = request.POST['fund_customer_number']

        if username.strip() == "":
            isvalid = False
            messages.warning(request, "请输入您的姓名！")
        if mobile.strip() == "":
            isvalid = False
            messages.warning(request, "请输入您的手机！")
        
        # if address.strip() == "":
        #     isvalid = False
        #     messages.warning(request, "请输入您的地址！")
        #
        # if email.strip() == "":
        #     isvalid = False
        #     messages.warning(request, "请输入您的Email地址！")
        #
        # if company.strip() == "":
        #     isvalid = False
        #     messages.warning(request, "请输入您的公司名称！")
        #
        # if job_title.strip() == "":
        #     isvalid = False
        #     messages.warning(request, "请输入您的职位！")
        #
        #
        # if household_spending == 0:
        #     isvalid = False
        #     messages.warning(request, "请选择您家庭的最大支出部分")
        #
        # if investment_apply == 0:
        #     isvalid = False
        #     messages.warning(request, "请选择您近期资金配资的安排")
        #
        # if investement_focus == 0:
        #     isvalid = False
        #     messages.warning(request, "请选择您在选择理财产品关注点")


        
        f['username']=username
        f['mobile']=mobile
        # f['address']=address
        # f['email']=email
        # f['company']=company
        # f['job_title']=job_title
        # f['hobby']=hobby
        # f['household_spending']=household_spending
        # f['investment_apply']=investment_apply
        # f['investement_focus']=investement_focus
        #f['fund_customer_number']=fund_customer_number
        
        if isvalid:
            user_num = UserProfile.objects.filter(user__first_name=username,mobile=mobile).count()
            if user_num >0:
                _user_profile=UserProfile.objects.filter(user__first_name=username,mobile=mobile).first()
                


                # if hobby.strip() !="":
                #     _user_profile.hobby = hobby
                # _user_profile.address=address
                #
                # _user_profile.company=company
                # _user_profile.job_title=job_title
                _user_profile.wx_openid=openid
                _user_profile.save()

                cash_event.user=_user_profile.user
            else:
                _user=User()
                max_id=User.objects.order_by('-id').first().id
                _user.username="XD"+str(max_id+1)
                _user.first_name=username
                _user.password=make_password(_user.username)
                #_user.email=email

                _user.save()
                _new_user=User.objects.filter(username=_user.username).order_by('-id').first()
                
                _profile = UserProfile()
                _profile.user=_new_user
                _profile.mobile=mobile
                # _profile.address=address
                # _profile.company=company
                # _profile.job_title=job_title
                # _profile.hobby=hobby
                _profile.wx_openid=openid
                _profile.source=4
                _profile.save()
                

                cash_event.user=_new_user

            # cash_event.household_spending=household_spending
            # cash_event.investment_apply=investment_apply
            # cash_event.investement_focus=investement_focus
            cash_event.introducer=c['introducer']
            try:
                _cash_record_num = CashEventInfo.objects.filter(user=cash_event.user).count()
                
                if _cash_record_num>0:
                    messages.success(request, "您已经报名参加过小金库活动！")

                else:
                    cash_event.status=1
                    cash_event.event_add_time=datetime.datetime.now()
                    cash_event.event_amount=Decimal(0)
                    cash_event.save()

                    #添加推荐记录
                    if cash_event.introducer !="":
                        introducer_num=UserProfile.objects.filter(wx_openid=cash_event.introducer).count()
                        if introducer_num>0:
                            introducer=UserProfile.objects.filter(wx_openid=cash_event.introducer).first()

                            #不能自己推荐自己
                            if introducer !=cash_event.user:
                                recommond_history=CashEventRecommondInfo()
                                recommond_history.user=cash_event.user
                                recommond_history.introducer=introducer.user
                                
                                #当月推荐人数封顶10人
                                start_date= datetime.date.today().replace(day=1)
                                end_date=(datetime.date.today().replace(day=1) + datetime.timedelta(31)).replace(day=1)
                                if CashEventRecommondInfo.objects.filter(introducer=introducer,add_time__gte=start_date,add_time__lt=end_date).count()<=10:
                                    recommond_history.amount=500
                                recommond_history.save()

                    #如果是基金客户直接给到10000虚拟货币
                    temp_user=UserProfile.objects.filter(user=cash_event.user).first()
                    if temp_user.is_investment==1:
                        
                        cash_event.event_amount=Decimal(10000)
                        cash_event.save()
                        return redirect('member.money')

                    isSuccess=True

                    return redirect('member.money')
                

            except Exception, e:
                    messages.warning(request,e)
            
    c['f']=f
    c['is_ok'] =isSuccess
    c['openid']=openid

    wechat = WechatBasic(token=WEIXIN_TOKEN,appid=APPID,appsecret=APPSECRET)
    ticket=getJsApiTicket(wechat)
    sign = Sign(ticket,"http://"+request.get_host()+request.get_full_path())
    c['sign']=sign.sign()
    c['appid']=APPID
    c['openid']=openid
    
    return render_to_response("event/cash_join.html",c, context_instance=RequestContext(request))

@csrf_protect
def join(request):
    c = {}
    c.update(csrf(request))
    isvalid = True
    event_apply = EventApply()

    if request.method == 'POST':
        username = request.POST['username']
        mobile = request.POST['mobile']
        #address = request.POST['address']
        event = int(request.POST['event'])

        if username.strip() == "":
            isvalid = False
            messages.warning(request, "请输入您的用户名！")
        if mobile.strip() == "":
            isvalid = False
            messages.warning(request, "请输入您的手机！")
        
        # if address.strip() == "":
        #     isvalid = False
        #     messages.warning(request, "请输入您的地址！")
        
        if event == 0:
            isvalid = False
            messages.warning(request, "请选择您要参加的活动")
        
        event_apply.username=username
        event_apply.mobile=mobile
        #event_apply.address=address
        event_apply.event=event

        if isvalid:
            item_num = EventApply.objects.filter(username=username,mobile=mobile,event=event).count()
            if item_num >0:
                messages.warning(request, "您已经报名参加过该活动！")
            else:
                try:
                    event_apply.save()
                    messages.success(request, "您已成功报名该活动,请随时关注活动动态!")

                except Exception, e:
                    messages.warning(request,e)

    c['f']=event_apply
    return render_to_response("event/join.html",c, context_instance=RequestContext(request))


