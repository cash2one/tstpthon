#-*-encoding:utf-8-*-
from wechat_sdk import WechatBasic
import time,requests
from weixin.models import GobalAccessToken
def getAccessToken(wechat):
    appid = wechat._WechatBasic__appid

    _items_num=GobalAccessToken.objects.filter(appid=appid).count()
    if _items_num >0:
        _item = GobalAccessToken.objects.filter(appid=appid).first()
        if _item.access_token_expires_at <= int(time.time()):
            _dict=wechat.get_access_token()
            _item.access_token=_dict.get('access_token','')
            _item.access_token_expires_at=_dict.get('access_token_expires_at',0)
            _item.save()

        return _item.access_token
    else:
        _item=GobalAccessToken()
        _dict=wechat.get_access_token()
        _item.appid=appid
        _item.access_token=_dict.get('access_token','')
        _item.access_token_expires_at=_dict.get('access_token_expires_at',0)
        _item.save()

        return _item.access_token

def getJsApiTicket(wechat):
    appid = wechat._WechatBasic__appid
    access_token=getAccessToken(wechat)

    _item = GobalAccessToken.objects.filter(appid=appid).first()
    if _item.js_api_ticket_expires_at <= int(time.time()):
        
        jsToken = getWechatJsApiTicketUrl(access_token)
        res = requests.get(jsToken)
        json = res.json()
        ticket = json["ticket"]
        expires_at = int(time.time())+json["expires_in"]
        _item.js_api_ticket=ticket
        _item.js_api_ticket_expires_at=expires_at
        _item.save()
    return _item.js_api_ticket
   

def getWechatAuthUrl(APPID, REDIRECT_URI, SCOPE, STATE):
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid="+APPID+"&redirect_uri="+REDIRECT_URI+"&response_type=code&scope="+SCOPE+"&state="+STATE+"#wechat_redirect"
    return url

def getWechatOauth2TokenUrl(APPID, APPSECRET, CODE):
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid="+APPID+"&secret="+APPSECRET+"&code="+CODE+"&grant_type=authorization_code"
    return url

def getWechatJsApiTicketUrl(ACCESS_TOKEN):
    url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token="+ACCESS_TOKEN+"&type=jsapi"
    return url

def getWechatUserInfoUrl(ACCESS_TOKEN, OPENID):
    url = "https://api.weixin.qq.com/sns/userinfo?access_token="+ACCESS_TOKEN+"&openid="+OPENID+"&lang=zh_CN"
    return url

