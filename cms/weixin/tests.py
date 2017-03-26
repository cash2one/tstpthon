import os,sys
sys.path.append(os.path.abspath('../'))
import olive.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "olive.settings")
#from django.test import TestCase
from wechat_sdk import WechatBasic
from oauth import getJsApiTicket,getAccessToken

wechat = WechatBasic(appid='wxf6b62f557ceff535', appsecret='639058f6e069390dd94727e073868d91')
#print wechat.get_access_token()
#print wechat.grant_token()
#print wechat.get_menu()
print getAccessToken(wechat)
print getJsApiTicket(wechat)
