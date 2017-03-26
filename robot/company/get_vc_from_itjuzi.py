# -*- coding: utf-8 -*- 
from api import get_html,bind_db,init_logging,Item,save_item

def mapper_item(soup):
    item=Item()

    item.name = soup.select('.public-info p a')[0].get_text()
    

    _img_list=soup.select('.media a img')        
    if len(_img_list)>0:
        item.logo=_img_list[0]['src']
        

    list1 = soup.select('.detail-info > li')
    
    for _item in list1:

        inner_list=_item.get_text().replace(u'：',':').split(':')
        if len(inner_list)>0:
            _inner_label=inner_list[0].strip()
            _inner_text=u''
            if len(inner_list)>1:
                _inner_text=unicode(inner_list[1].strip())
           
            if _inner_label ==u'网址':
                if len(inner_list)>2:
                    item.website=inner_list[2].replace('//','').strip()
            
            if _inner_label ==u'阶段':
                item.stage=_inner_text
            
            if _inner_label ==u'介绍':
                item.desc=_inner_text

            if _inner_label ==u'领域':
                item.field=_inner_text


    return item

logging=init_logging()
session,query=bind_db('itjuzi_vc')


start_id=1473
end_id=1494

for num in range(start_id,end_id+1):
    print num
    try:
        _soup=get_html('http://itjuzi.com/investfirm/'+str(num))
        _item=mapper_item(_soup)
        print _item.name,_item.logo,_item.desc
        save_item(session,query,_item)
    
    except Exception,e:
        print e
        logging.error(e)

