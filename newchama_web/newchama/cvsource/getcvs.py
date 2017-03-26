#-*-encoding:utf-8-*-
import os,sys
sys.path.append(os.path.abspath('..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
#from django.conf import settings
#settings.configure()

import json
import urllib2
import hashlib
import datetime
from cvsource.models import BuyTogether,BuyEp

yesterday = datetime.datetime.now()+datetime.timedelta(days=-30)
date_str = yesterday.strftime('%Y-%m-%d')

AppKeyid='00004'
AppKey='D03D17C25A9A1F4B'

current_pageNo=1

request_dic = {'sysAppkey':AppKeyid, 'sysMethod':'cv.web.event.buytogether.list', 'sysV':'1.0', 'searchData':date_str, 'sysFormat':'json','sysLocal':'en','pageNo':current_pageNo}

pre_url=r'http://openapi.chinaventure.com.cn/router?'

currency_to_usd={
u'万元':1/6.1306,
u'万加元':1/1.0961,
u'万台币':1/29.9790,
u'万新元':1/1.2635,
u'万新西兰元':0.8188,
u'万日元':1/106.8900,
u'万欧元':1.2911,
u'万港元':1/7.7497,
u'万澳元':0.9184,
u'万美元':1,
u'万英镑':1.6202,
u'万韩元':1/1036
}


def buildRequestString(keyid,key,dic,pre_url):
	
	sort_list = sorted(dic.iteritems(), key=lambda d:d[0], reverse = False ) 
	code=''
	for item in sort_list: 
		code+=str(item[0])+str(item[1])

	request_str = ''
	for item in dic:
		request_str+=item+'='+str(dic[item])+'&'

	request_str += 'sysSign='+str.upper(hashlib.sha1(key+code+key).hexdigest())
	
	return pre_url+request_str

def saveRecord(item):
	buy_record =TansJsonToBuyTogether(item)
	old_buy_record=BuyTogether.objects.filter(tBuyID=buy_record.tBuyID)
	if len(old_buy_record) == 0:
		buy_record.save()
		if item.has_key('buyEpList'):
			for buy_item in item['buyEpList']:
				temp_buyep=TansJsonToBuyEp(buy_item)
				buy_record.buyep_set.add(temp_buyep)
		print('%s saved!' % (buy_record))
	else:
		print('%s is existed!' % (buy_record))


def getRecordByNO(pageNo):

	request_dic['pageNo']=current_pageNo
	url=buildRequestString(AppKeyid,AppKey,request_dic,pre_url)
	html = urllib2.urlopen(url)

	jsonobj = json.loads(html.read().decode('utf-8'))

	
	if pageNo==1:
		print("="*80)
		print("date:"+date_str+"   total count:"+str(jsonobj['page']['totalCount']))
		print("="*80)

	for item in jsonobj['list']:
		#print(item['cnName']+"-"+unicode(item['money'])+unicode(item['currency']))
		saveRecord(item)
		

	return jsonobj['page']['totalPages']

def TansJsonToBuyTogether(json_obj):

	buytogether=BuyTogether()

	buytogether.tBuyID=json_obj['tBuyID']
	buytogether.cnName=json_obj['cnName']
	buytogether.money=json_obj['money']
	buytogether.currency=json_obj['currency']

	
	currency_usd=currency_to_usd.get(unicode(json_obj['currency']).strip(),1)
	print currency_usd
	if buytogether.money!=None :
		buytogether.usd=float(buytogether.money)*currency_usd

	buytogether.type=json_obj['type']
	buytogether.tBuyWay=json_obj['tBuyWay']
	buytogether.attitudeName=json_obj['attitudeName']
	buytogether.state=json_obj['state']
	buytogether.happenDate=json_obj['happenDate']
	buytogether.endDate=json_obj['endDate']
	buytogether.dstrict=json_obj['dstrict']
	buytogether.whetherTrade=json_obj['whetherTrade']
	#buytogether.stockRightPercent=json_obj['stockRight']
	if json_obj['stockRight'].endswith('%'):
		if unicode(json_obj['stockRight'][0:-1]).isdigit():
			buytogether.stockRightPercent=json_obj['stockRight'][0:-1]
	else:
		if unicode(json_obj['stockRight']).isdigit():
			buytogether.stockRightPercent=json_obj['stockRight']

	buytogether.desc=json_obj['desc']
	buytogether.payStyle=json_obj['payStyle']
	buytogether.cvIndustryOne=json_obj['cvIndustryOne']
	buytogether.cvIndustryTwo=json_obj['cvIndustryTwo']
	buytogether.cvIndustryThree=json_obj['cvIndustryThree']
	buytogether.gbIndustryOne=json_obj['gbIndustryOne']
	buytogether.gbIndustryTwo=json_obj['gbIndustryTwo']
	buytogether.gbIndustryThree=json_obj['gbIndustryThree']
	buytogether.gbIndustryFour=json_obj['gbIndustryFour']
	buytogether.swIndustryOne=json_obj['swIndustryOne']
	buytogether.swIndustryTwo=json_obj['swIndustryTwo']
	buytogether.swIndustryThree=json_obj['swIndustryThree']
	buytogether.zjIndustryOne=json_obj['zjIndustryOne']
	buytogether.zjIndustryTwo=json_obj['zjIndustryTwo']
	buytogether.zjIndustryThree=json_obj['zjIndustryThree']
	buytogether.zjIndustryFour=json_obj['zjIndustryFour']
	buytogether.epCnName=json_obj['epCnName']
	buytogether.epCnShortName=json_obj['epCnShortName']
	buytogether.epEnName=json_obj['epEnName']
	buytogether.epEnShortName=json_obj['epEnShortName']

	for index,address_item in enumerate(json_obj['epAddress'].split('>')):
		if index==0:
			buytogether.epAddress1=address_item
		elif index==1:
			buytogether.epAddress2=address_item
		elif index==2:
			buytogether.epAddress3=address_item
		elif index==3:
			buytogether.epAddress4=address_item
		elif index==4:
			buytogether.epAddress5=address_item
		else:
			pass

	return buytogether

def TansJsonToBuyEp(json_obj):

	buyep=BuyEp()

	buyep.cnName=json_obj['cnName']
	buyep.cnShortName=json_obj['cnShortName']
	buyep.enName=json_obj['enName']
	buyep.enShortName=json_obj['enShortName']

	return buyep


if __name__=="__main__":
    
	totlePageNum=getRecordByNO(current_pageNo)

	if totlePageNum>1:
		for i in range(2,totlePageNum):
			current_pageNo=i
			getRecordByNO(current_pageNo)

	
		




