#-*-encoding:utf-8-*-
from django.shortcuts import render,render_to_response, redirect, HttpResponse, RequestContext, get_object_or_404
from wechat_sdk import WechatBasic
from django.views.decorators.csrf import csrf_exempt 
import hashlib
import json
#from lxml import etree
from django.utils.encoding import smart_str


WEIXIN_TOKEN = 'olive2015'

def qa(request):
    return render_to_response("home/qa.html", context_instance=RequestContext(request))



def about(request):
    return render_to_response("home/about.html", context_instance=RequestContext(request))


def project(request):

    return render_to_response("home/project.html", context_instance=RequestContext(request))

def thinking(request):
    return render_to_response("home/thinking.html", context_instance=RequestContext(request))





@csrf_exempt
def weixin(request):
    """
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    """
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = WEIXIN_TOKEN
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("weixin  index")
    else:
        xml_str = smart_str(request.body)
        signature = request.GET.get("signature", None)
        #request_xml = etree.fromstring(xml_str)
        response_xml = auto_reply_main(xml_str)# 修改这里
        return HttpResponse(response_xml)

def auto_reply_main(request_xml):
    body_text = """
    <xml>
    <ToUserName><![CDATA[xiandetouzi]]></ToUserName>
    <FromUserName><![CDATA[ofzKZt8-IP2RblntwlrOg3B_i2OI]]></FromUserName>
    <CreateTime>1422802897</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[hkkhkjjj]]></Content>
    <MsgId>1234567890abcdef</MsgId>
    </xml>
    """

    return request_xml