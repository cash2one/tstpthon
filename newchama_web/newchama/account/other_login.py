#-*-encoding:utf-8-*-
import json
from django.contrib import messages
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import RequestContext
from weibo_api import ctx, get, post, route, seeother, forbidden, jsonresult, Template
from weibo import APIError, APIClient
from django.shortcuts import render, render_to_response, redirect, get_object_or_404, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from newchama import settings
from services.models import OtherLogin, Member, LoginType
import logging
import simplejson, datetime
from log.views import *
from newchama.helper import saveOtherLogin, buildMemberForFront, checkOtherLogin
logger = logging.getLogger(__name__)

#pip install sinaweibopy

APP_KEY = '2229229848' # app key
APP_SECRET = 'f32fdbfd76e13cd54551e2c0876ed79e' # app secret
CALLBACK_URL = 'http://www.newchama.com/account/weibo' # callback url
CANCEL_CALLBACK_URL = 'http://www.newchama.com/account/cancel_weibo' # callback url

def weibo(request):
    c = {}
    client = _create_client()
    code = request.GET.get('code', '')
    if code != "":
        try:
            r = client.request_access_token(code)
            access_token, expires_in, uid = r.access_token, r.expires_in, r.uid
            # client.set_access_token(access_token, expires_in)
            # ol = OtherLogin.objects.get(uid=uid)
            ols = OtherLogin.objects.filter(uid=uid)[:1]
            ol = OtherLogin()
            member = Member()
            if ols:
                ol = ols[0]
            ol.access_token = access_token
            ol.login_type = LoginType.weibo
            ol.expires_in = expires_in
            ol.uid = uid
            ol.save()
            members = Member.objects.filter(weibo=ol.id)[:1]
            if members:
                member = members[0]
                member.last_login_time = datetime.datetime.now()
                login_count = member.login_count
                member.login_count += 1
                member.save()
                if login_count == 0:
                    write_login_log(request, member, 'setting_first')
                    return redirect("other_login.first")

                role = ""
                request.session["member"] = buildMemberForFront(request, member, role)
                if request.GET.get('back_url',None):
                    write_login_log(request, member, request.GET['back_url'])
                    return redirect(request.GET['back_url'])
                else:
                    write_login_log(request, member, 'index')
                    return redirect('account.index')
                c['username'] = username
            else:
                request.session["other_login"] = saveOtherLogin(access_token, ol.id, expires_in, LoginType.weibo)
                # return render_to_response("account/"+request.lang+"/signup.html", c, context_instance=RequestContext(request))
                return render_to_response("account/"+request.lang+"/first_other_login.html", c, context_instance=RequestContext(request))
        except Exception, e:
            logger.error(e)
    c['title'] = _("Login")
    response = render_to_response("account/"+request.lang+"/login.html", c, context_instance=RequestContext(request))
    return response


def signin(request):
    client = _create_client()
    return redirect(client.get_authorize_url())


@csrf_protect
def first(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        otherLogin = request.session.get('other_login', None)
        if otherLogin is None:
            return render_to_response("account/"+request.lang+"/login.html", c, context_instance=RequestContext(request))
        else:
            ol = checkOtherLogin(otherLogin)
            if ol:
                username = request.POST['username']
                password = request.POST['password']
                role = ""
                m, bool = Member.login(username, password)
                if bool is False:
                    messages.error(request, m)
                else:
                    request.session["other_login"] = None
                    if m.status == 4:
                        write_login_log(request,m,'active_error')
                        return redirect('account.active_error')

                    if m.status == 3:
                        write_login_log(request,m,'must_change_password')
                        return redirect('account.must_change_password')

                    request.session["member"] = buildMemberForFront(request, m, role)

                    m.last_login_time = datetime.datetime.now()
                    login_count = m.login_count
                    m.login_count += 1
                    m.weibo_id = ol.id
                    m.save()

                    if login_count == 0:
                        write_login_log(request,m,'setting_first')
                        return redirect("account.setting_first")

                    if request.GET.get('back_url',None):
                        write_login_log(request,m,request.GET['back_url'])
                        return redirect(request.GET['back_url'])
                    else:
                        write_login_log(request,m,'index')
                        return redirect('account.index')

                c['username'] = username
            c['title'] = _("Login")
            response = render_to_response("account/"+request.lang+"/first_other_login.html", c, context_instance=RequestContext(request))
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, request.lang)
            return response
    response = render_to_response("account/"+request.lang+"/login.html", c, context_instance=RequestContext(request))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, request.lang)
    return response


def _create_client():
    return APIClient(APP_KEY, APP_SECRET, CALLBACK_URL)