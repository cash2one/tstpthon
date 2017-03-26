#-*-encoding:utf-8-*-

import os,sys
sys.path.append(os.path.abspath('../'))
import olive.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "olive.settings")
#from django.test import TestCase
from wechat_sdk import WechatBasic
from weixin.views import APPID,APPSECRET


def set_menu():
    wechat = WechatBasic(appid=APPID, appsecret=APPSECRET)
    wechat.create_menu({
        'button':[
            {
                'name':u'功能测试',
                'sub_button':[
                    {
                        'type':'view',
                        'name':u'JS-SDK',
                        'url':'http://cms.olive-app.com/weixin/testjs/'
                    }
                ]
            },
            {
                'name':u'菜单2',
                'sub_button':[
                    {
                        'type':'view',
                        'name':u'个人中心',
                        'url':'http://xiande.olive-app.com/member/'
                    },
                    {
                        'type':'view',
                        'name':u'个人资产',
                        'url':'http://xiande.olive-app.com/member/assets/'
                    },
                    {
                        'type':'view',
                        'name':u'我要理财',
                        'url':'http://xiande.olive-app.com/member/join/'
                    },
                    {
                        'type':'view',
                        'name':u'个人小金库',
                        'url':'http://xiande.olive-app.com/member/money/'
                    }
                ]
            },
            {
                'name':u'菜单3',
                'sub_button':[
                    {
                        'type':'click',
                        'name':u'热门活动',
                        'key':'event_hot'
                    },
                    {
                        'type':'click',
                        'name':u'本月活动',
                        'key':'event_month'
                    },
                    {
                        'type':'view',
                        'name':u'我要报名',
                        'url':'http://xiande.olive-app.com/event/join/'
                    }
                ]
            }
        ]})