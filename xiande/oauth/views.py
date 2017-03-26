#-*-encoding:utf-8-*-
from django.shortcuts import render, HttpResponse, redirect
from wechat_sdk import WechatBasic
import requests
from django.views.decorators.csrf import csrf_exempt 


WEIXIN_TOKEN = 'olive2015'


# Create your views here.
def index(request):
    APPID = "wx89e2b26a517ddf7c"
    APPSECRET = "a1e1237b4524c133734e0d8ba0a3bb74"
    token = WEIXIN_TOKEN
    REDIRECT_URI = "http://"+request.get_host()+request.get_full_path()
    SCOPE = "snsapi_userinfo"
    STATE = "olive"
    request_code = request.GET.get("code", "")
    if request_code != "":
        urlToken = getWechatTokenUrl(APPID, APPSECRET, request_code)
        res = requests.get(urlToken)
        json = res.json()
        openid = json["openid"]
        access_token = json["access_token"]
        request.session["openid"] = openid
        request.session["access_token"] = access_token
        urlUserInfo = getWecharUserInfoUrl(access_token, openid)
        ures = requests.get(urlUserInfo)
        ujson = ures.json()
        nickname = ujson["nickname"]
        city = ujson["city"]
        headimgurl = ujson["headimgurl"]
        request.session["nickname"] = nickname
        request.session["city"] = city
        request.session["headimgurl"] = headimgurl
        refer = request.GET.get("refer", "")
        if refer != "":
            return redirect(refer)
        return HttpResponse(ures.text)
    openid = request.session.get("openid", "")
    if openid == "":
        urlAuth = getWechatAuthUrl(APPID, REDIRECT_URI, SCOPE, STATE)
        return redirect(urlAuth)

def getWechatAuthUrl(APPID, REDIRECT_URI, SCOPE, STATE):
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid="+APPID+"&redirect_uri="+REDIRECT_URI+"&response_type=code&scope="+SCOPE+"&state="+STATE+"#wechat_redirect"
    return url

def getWechatTokenUrl(APPID, APPSECRET, CODE):
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid="+APPID+"&secret="+APPSECRET+"&code="+CODE+"&grant_type=authorization_code"
    return url

def getWecharUserInfoUrl(ACCESS_TOKEN, OPENID):
    url = "https://api.weixin.qq.com/sns/userinfo?access_token="+ACCESS_TOKEN+"&openid="+OPENID+"&lang=zh_CN"
    return url