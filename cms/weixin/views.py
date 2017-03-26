#-*-encoding:utf-8-*-
from django.shortcuts import render,render_to_response, redirect, HttpResponse, RequestContext, get_object_or_404
from wechat_sdk import WechatBasic
from django.views.decorators.csrf import csrf_exempt 
import hashlib
import json
#from lxml import etree
from django.utils.encoding import smart_str
from oauth import getWechatAuthUrl,getWechatOauth2TokenUrl,getWechatJsApiTicketUrl,getWechatUserInfoUrl,getAccessToken,getJsApiTicket
from sign import Sign

'''
OliveSoftware
'''
APPID = "wx458e8072932a2a3e"
APPSECRET = "37566cd850e3624b42981224485e6612"


WEIXIN_TOKEN = 'olive2015'

@csrf_exempt
def index(request):
    """
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    """
    return_str=''
    signature = request.GET.get("signature", None)
    timestamp = request.GET.get("timestamp", None)
    nonce = request.GET.get("nonce", None)
    echostr = request.GET.get("echostr", None)

    if request.method == "GET":
        
        
        tmp_list = [WEIXIN_TOKEN, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return_str=echostr
        else:
            return_str="weixin  index"
            
    else:
        body_text = smart_str(request.body)

        wechat = WechatBasic(token=WEIXIN_TOKEN)
        # 对签名进行校验
        if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            # 对 XML 数据进行解析 (必要, 否则不可执行 response_text, response_image 等操作)
            wechat.parse_data(body_text)
            # 获得解析结果, message 为 WechatMessage 对象 (wechat_sdk.messages中定义)
            message = wechat.get_message()

            
            # 现在直接将 response 变量内容直接作为 HTTP Response 响应微信服务器即可，此处为了演示返回内容，直接将响应进行输出
            return_str = weixin_main(wechat,message)

    return HttpResponse(return_str)

def testjs(request):
    c = {}
    wechat = WechatBasic(token=WEIXIN_TOKEN,appid=APPID,appsecret=APPSECRET)
    ticket=getJsApiTicket(wechat)
    sign = Sign(ticket,"http://"+request.get_host()+request.get_full_path())
    c['sign']=sign.sign()
    c['appid']=APPID
    return render_to_response("weixin/testjs.html", c, context_instance=RequestContext(request))


def oauth(request):
    """
    网页认证
    """
    token = WEIXIN_TOKEN
    REDIRECT_URI = "http://"+request.get_host()+request.get_full_path()
    SCOPE = "snsapi_userinfo"
    STATE = "olive"
    request_code = request.GET.get("code", "")
    if request_code != "":
        urlToken = getWechatOauth2TokenUrl(APPID, APPSECRET, request_code)
        res = requests.get(urlToken)
        json = res.json()
        openid = json["openid"]
        access_token = json["access_token"]
        request.session["openid"] = openid
        request.session["access_token"] = access_token
        urlUserInfo = getWechatUserInfoUrl(access_token, openid)
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


def weixin_main(wechat,message):
    response = None

    if message.type == 'text':
        if message.content == 'wechat':
            response = wechat.response_text(u'^_^')
        else:
            response = wechat.response_text(u'文字')
    elif message.type == 'image':
        response = wechat.response_text(u'图片')
    
    elif message.type == 'click' and message.key == 'event_hot':
        response = wechat.response_news([
            {
                'title': u'第一条新闻标题',
                'description': u'第一条新闻描述，这条新闻没有预览图',
                'url': u'http://www.google.com.hk/',
            }, {
                'title': u'第二条新闻标题, 这条新闻无描述',
                'picurl': u'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
                'url': u'http://www.github.com/',
            }, {
                'title': u'第三条新闻标题',
                'description': u'第三条新闻描述',
                'picurl': u'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
                'url': u'http://www.v2ex.com/',
            }
        ])

    else:
        response = wechat.response_text(u'未知')

    return response
