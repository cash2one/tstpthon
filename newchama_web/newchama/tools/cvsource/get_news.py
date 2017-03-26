# -*- coding: utf-8 -*-  
import logging

logging.basicConfig(level=logging.ERROR,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='news_error.log',
                filemode='a')
try:
    import datetime
    import json
    import urllib2
    from api import buildRequestString,AppKeyid,AppKey,initDB,convert_time


    date_str = (datetime.datetime.now()+datetime.timedelta(days=-60)).strftime('%Y-%m-%d')

    class NewsItem(object):   
        pass


    current_pageNo=1

    request_dic = {'sysAppkey':AppKeyid, 'sysMethod':'cv.web.event.news.list', 'sysV':'1.0', 'searchDate':date_str, 'sysFormat':'json','pageNo':current_pageNo}
    pre_url=r'http://openapi.chinaventure.com.cn/router?'

    session,query = initDB('cvsource_news',NewsItem)


    def saveRecord(item):
        
        _item=NewsItem()
        _item.title=item['newsTitle']
        _item.content=item['newsContent']
        _item.tag=item['newsTag']

        _item.time=convert_time(item['newsPusDate'])
        
        _item.add_time= datetime.datetime.now()

        c = query.filter_by(title=_item.title).first()
        
        if c:
            pass
            #print 'Exist:',_item.title
        else:
            session.add(_item)
            #print 'Add:',_item.title
        
        session.flush()
        session.commit()

        

    def getRecordByNO(pageNo):

        request_dic['pageNo']=current_pageNo
        url=buildRequestString(AppKeyid,AppKey,request_dic,pre_url)
        print url
        html = urllib2.urlopen(url)

        jsonobj = json.loads(html.read().decode('utf-8'))
       
        if pageNo==1:
            '''
            print("="*80)
            print("date:"+date_str+"   total page count:"+str(jsonobj['page']['totalCount']))
            print("="*80)
            '''
            pass

        for item in jsonobj['list']:
            saveRecord(item)
            
        return jsonobj['page']['totalPages']


    if __name__=="__main__":

        try:    
            totlePageNum=getRecordByNO(current_pageNo)

            if totlePageNum>1:
                for i in range(2,totlePageNum+1):
                    current_pageNo=i
                    getRecordByNO(current_pageNo)

        except Exception,e:
            logging.error(e)

except Exception,e:
            logging.error(e)



