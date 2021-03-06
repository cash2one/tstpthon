#-*-encoding:utf-8-*-

from wechat_sdk import WechatBasic

def set_menu():
    wechat = WechatBasic(appid='wxf6b62f557ceff535', appsecret='639058f6e069390dd94727e073868d91')
    wechat.create_menu({
        'button':[
            {
                'name':u'金融服务',
                'sub_button':[
                    {
                        'type':'view',
                        'name':u'关于我们',
                        'url':'http://xiande.olive-app.com/about/'
                    },
                    {
                        'type':'view',
                        'name':u'投资理念',
                        'url':'http://xiande.olive-app.com/thinking/'
                    },
                    {
                        'type':'view',
                        'name':u'理财产品',
                        'url':'http://xiande.olive-app.com/project/'
                    }
                ]
            },
            {
                'name':u'理财管家',
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
                'name':u'超值享',
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

set_menu()
