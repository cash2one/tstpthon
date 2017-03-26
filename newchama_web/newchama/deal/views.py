#-*-encoding:utf-8-*-
from django.shortcuts import render
from django.shortcuts import render,render_to_response, redirect, get_object_or_404, HttpResponse, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from services.models import StatusProject,StatusDemand,Member, Deal,ListDeal,TransDeal,BuyTogetherDeal,PreferenceIndustry,Project,Demand,Industry,Country,TempUsDeal
from newchama.helper import member_login_required

from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils import simplejson
from django.db.models import Count,Sum,Q

from django.template import loader
from django.contrib import messages
import datetime
import logging
logger = logging.getLogger(__name__)


@member_login_required
def index(request, type):
    
    c = {}
    c['title']=_("Deal List")
    c['deal_list'] =Deal.objects.order_by('-update_time')[0:10]
    c['deal_total'] = Deal.objects.count()
    c['member'] = request.session.get('member', None)
    c['type'] = type
    
    if c['member']:
        preference_list=PreferenceIndustry.objects.filter(preference__member__id=c['member']['id'])

        c['preference_list']=list(set([item.industry for item in preference_list])) 
        
    c['active_idx']=0

    c['p_list']=Project.objects.order_by('-pv').filter(is_public=True,expire_date__gt=datetime.datetime.now(),status=StatusProject.approved)[0:5]

    c['d_list']=Demand.objects.order_by('-pv').filter(target_members=None,target_companies=None,target_industries=None,expire_date__gt=datetime.datetime.now(),status=StatusDemand.approved)[0:5]
    c['hidden_industry_id']=0

    c['hidden_can_clicked']=1

    if request.is_cn:
        c['industry_name'] = '全部'
    else:
        c['industry_name'] = 'All'

    return render_to_response("deal/"+request.lang+"/list.html", c, context_instance=RequestContext(request))

@member_login_required
def industry(request,id):
    c = {}
    c['title']=_("Deal List")

    industry = get_object_or_404(Industry, pk=id)

   
    if industry.level==3:
        c['hidden_industry_id']=industry.father.id;

        c['deal_list'] = Deal.objects.filter(cv3=id).order_by('-update_time')[0:10]
        c['deal_total'] = Deal.objects.filter(cv3=id).count()

    elif industry.level==2:
        c['hidden_industry_id']=industry.id;
        c['deal_list'] = Deal.objects.filter(cv2=id).order_by('-update_time')[0:10]
        c['deal_total'] = Deal.objects.filter(cv2=id).count()

    else:
        c['hidden_industry_id']=industry.id;
        c['deal_list'] = Deal.objects.filter(cv1=id).order_by('-update_time')[0:10]
        c['deal_total'] = Deal.objects.filter(cv1=id).count()
    

    
    c['member'] = request.session.get('member', None)

    if c['member']:
        preference_list=PreferenceIndustry.objects.filter(preference__member__id=c['member']['id'])

        c['preference_list']=list(set([item.industry for item in preference_list])) 
    
    if industry in c['preference_list']:
        c['active_idx']=c['preference_list'].index(industry)+1
    else:
        c['active_idx']=0

        c['p_list']=Project.objects.order_by('-pv').filter(is_public=True,expire_date__gt=datetime.datetime.now(),status=StatusProject.approved)[0:5]

        c['d_list']=Demand.objects.order_by('-pv').filter(target_members=None,target_companies=None,target_industries=None,expire_date__gt=datetime.datetime.now(),status=StatusDemand.approved)[0:5]
    c['industry_id'] = id

    if request.is_cn:
        c['industry_name'] = industry.name_cn
    else:
        c['industry_name'] = industry.name_en

    c['hidden_can_clicked']=1

    return render_to_response("deal/"+request.lang+"/list.html", c, context_instance=RequestContext(request))




@member_login_required
def country(request,id=0):
    c = {}
    c['title']=_("Deal List")

    day=365
    start_date = datetime.datetime.now()+datetime.timedelta(days=-day)

    c['cn_id']=str(get_object_or_404(Country,name_en='China').id)
    c['us_id']=str(get_object_or_404(Country,name_en='United States of America').id)
    deals = Deal.objects.all()
    if int(id) > 0:
        deals = deals.filter(country_id=id)
    c['deal_list'] = deals.order_by('-update_time')[0:10]
    c['deal_total'] = deals.count()
    c['member'] = request.session.get('member', None)
    

    c['hidden_country_id']=str(id)

    c['p_list']=Project.objects.order_by('-pv').filter(is_public=True,expire_date__gt=datetime.datetime.now(),status=StatusProject.approved)[0:5]

    c['d_list']=Demand.objects.order_by('-pv').filter(target_members=None,target_companies=None,target_industries=None,expire_date__gt=datetime.datetime.now(),status=StatusDemand.approved)[0:5]
    
    c['country_id'] = id
    c['hidden_is_cv1']=1
        
    if int(id) > 0:
        condtion1=Q(happen_date__gt=start_date,country_id=id)
    else:
        condtion1=Q(happen_date__gt=start_date)

    c['last_num1']=Deal.objects.filter(condtion1).count()
    c['last_num2']=Deal.objects.filter(condtion1).aggregate(Sum('amount_usd'))['amount_usd__sum']/1000000

    top_industry_id=Deal.objects.exclude(cv1=None).filter(condtion1).values('cv1').annotate(num_all=Count('id')).order_by('-num_all')[:1]
    # print '*'*80
    # print top_industry_id[0]['cv1']
    # print '*'*80


    _industry=get_object_or_404(Industry,pk=top_industry_id[0]['cv1'])
    
    c['last_text1']=_industry.name_cn

    c['last_num3']=Deal.objects.filter(condtion1,cv1=_industry.id).count()
    c['last_num4']=Deal.objects.filter(condtion1,cv1=_industry.id).aggregate(Sum('amount_usd'))['amount_usd__sum']/1000000



    return render_to_response("deal/"+request.lang+"/country.html", c, context_instance=RequestContext(request))

USA_INDUSTRY={
    1:'B2B',2:'B2C',3:'Energy',4:'Financial Services',5:'Healthcare',6:'IT',7:'Materials & Resources'
}

USA_INDUSTRY_CN={
    1:'B2B',2:'B2C',3:'能源',4:'金融服务',5:'健康医疗',6:'IT',7:'材料及资源'
}
USA_DEAL_TYPE_CN={
    1:'融资',2:'并购',3:'增发',4:'定向增发',5:'IPO'
    
}
USA_DEAL_TYPE={
    1:'Financing',2:'Buyout',3:'Additonal issue',4:'Directed additional',5:'IPO'
    
}

@member_login_required
def rank(request):
    day=365
    
    num=int(request.GET.get('num',10))
    chart_type=int(request.GET.get('chart_type',0))
    country_id=int(request.GET.get('country_id',0))
    industry_id=int(request.GET.get('industry_id',0))
    deal_type=int(request.GET.get('deal_type',99))

    result={'is_ok':0,'error':''}

    start_date = datetime.datetime.now()+datetime.timedelta(days=-day)

    temp_list1={}
    
    result['is_ok']=1


    if country_id==212:

        if deal_type!=99:

            condtion1=Q(deal_type=deal_type)
        else:
            condtion1=Q()
        
        if chart_type==0:
            chart_type=2

        top_list=TempUsDeal.objects.filter(condtion1,chart_type=chart_type).order_by('-amount_usd')
        # print top_list
        # print '*'*80
        for item in top_list:

            if chart_type==1:
                item.amount_usd=item.amount_usd*1000000
            
            if request.is_cn:
                temp_list1[USA_INDUSTRY_CN[item.industry_id]]=[0,int(item.amount_usd)]
            else:
                temp_list1[USA_INDUSTRY[item.industry_id]]=[0,int(item.amount_usd)]


        result['top_list']=temp_list1

        return HttpResponse(simplejson.dumps(result))


    
    condtion1=Q(happen_date__gt=start_date)

    if deal_type!=99:
        condtion1=condtion1 & Q(deal_type=deal_type)
    
    
    if country_id != 0:
        condtion1=condtion1 & Q(country_id=country_id)
    try:
        if industry_id==0:
            if chart_type ==0:
                top_list=Deal.objects.exclude(cv1=None).exclude(cv1=130).filter(condtion1).values('cv1').annotate(   num_all=Count('id')).order_by('-num_all')[:num]
            else:
                top_list=Deal.objects.exclude(cv1=None).exclude(cv1=130).filter(condtion1).values('cv1').annotate(num_all=Sum('amount_usd')).order_by('-num_all')[:num]

            for item in top_list:
                _industry=get_object_or_404(Industry,pk=item['cv1'])
                if request.is_cn:
                    temp_list1[_industry.name_cn]=[_industry.id,int(item['num_all'])]
                else:
                    temp_list1[_industry.name_en]=[_industry.id,int(item['num_all'])]
        else:
            industry=get_object_or_404(Industry,pk=industry_id)
            if industry.level == 1:
                if chart_type ==0:
                    top_list=Deal.objects.exclude(cv2=None).filter(condtion1,cv1=industry.id).values('cv2').annotate(num_all=Count('id')).order_by('-num_all')[:num]
                else:
                    top_list=Deal.objects.exclude(cv2=None).filter(condtion1,cv1=industry.id).values('cv2').annotate(num_all=Sum('amount_usd')).order_by('-num_all')[:num]

                for item in top_list:
                    _industry=get_object_or_404(Industry,pk=item['cv2'])
                    if request.is_cn:
                        temp_list1[_industry.name_cn]=[_industry.id,int(item['num_all'])]
                    else:
                        temp_list1[_industry.name_en]=[_industry.id,int(item['num_all'])]
            elif industry.level == 2:
                if chart_type ==0:
                    top_list=Deal.objects.exclude(cv3=None).filter(condtion1,cv2=industry.id).values('cv3').annotate(num_all=Count('id')).order_by('-num_all')[:num]
                else:
                    top_list=Deal.objects.exclude(cv3=None).filter(condtion1,cv2=industry.id).values('cv3').annotate(num_all=Sum('amount_usd')).order_by('-num_all')[:num]

                for item in top_list:
                    _industry=get_object_or_404(Industry,pk=item['cv3'])
                    if request.is_cn:
                        temp_list1[_industry.name_cn]=[_industry.id,int(item['num_all'])]
                    else:
                        temp_list1[_industry.name_en]=[_industry.id,int(item['num_all'])]
    except:
        result['error']=ugettext('Something is error!')

    result['top_list']=temp_list1
    print(result)

    return HttpResponse(simplejson.dumps(result))

@member_login_required
def rank_deal_type(request):
    day=365
    num=10
    chart_type=int(request.GET.get('chart_type',0))
    country_id=int(request.GET.get('country_id',0))
    industry_id=int(request.GET.get('industry_id',0))
    

    result={'is_ok':0,'error':''}

    start_date = datetime.datetime.now()+datetime.timedelta(days=-day)

    temp_list1={}
    
    result['is_ok']=1


    if country_id==212:

        if chart_type==0:
            chart_type=2

        top_list=TempUsDeal.objects.filter(chart_type=chart_type).values('deal_type').annotate(num_all=Sum('amount_usd')).order_by('-num_all')

        for item in top_list:
            # print item
            if request.is_cn:
                temp_list1[USA_DEAL_TYPE_CN[item['deal_type']]]=int(item['num_all'])
            else:
                temp_list1[USA_DEAL_TYPE[item['deal_type']]]=int(item['num_all'])

        result['top_list']=temp_list1

        return HttpResponse(simplejson.dumps(result))

    
    condtion1=Q(happen_date__gt=start_date)
    
    if country_id != 0:
        condtion1=condtion1 & Q(country_id=country_id)
    try:
        if industry_id==0:
            if chart_type ==0:
                top_list=Deal.objects.exclude(deal_type=None).filter(condtion1).values('deal_type').annotate(num_all=Count('id')).order_by('-num_all')[:num]
            else:
                top_list=Deal.objects.exclude(deal_type=None).filter(condtion1).values('deal_type').annotate(num_all=Sum('amount_usd')).order_by('-num_all')[:num]


            for item in top_list:
               
                temp_list1[item['deal_type']]=int(item['num_all'])
        else:
            industry=get_object_or_404(Industry,pk=industry_id)
            if industry.level == 1:
                if chart_type ==0:
                    top_list=Deal.objects.exclude(deal_type=None).filter(condtion1,cv1=industry.id).values('deal_type').annotate(num_all=Count('id')).order_by('-num_all')[:num]
                else:
                    top_list=Deal.objects.exclude(deal_type=None).filter(condtion1,cv1=industry.id).values('deal_type').annotate(num_all=Sum('amount_usd')).order_by('-num_all')[:num]
    
                for item in top_list:
                    
                    temp_list1[item['deal_type']]=int(item['num_all'])
            elif industry.level == 2:
                if chart_type ==0:
                    top_list=Deal.objects.exclude(deal_type=None).filter(condtion1,cv2=industry.id).values('deal_type').annotate(num_all=Count('id')).order_by('-num_all')[:num]
                else:
                    top_list=Deal.objects.exclude(deal_type=None).filter(condtion1,cv2=industry.id).values('deal_type').annotate(num_all=Sum('amount_usd')).order_by('-num_all')[:num]
    
                for item in top_list:
                    
                    temp_list1[item['deal_type']]=int(item['num_all'])

            elif industry.level == 3:
                if chart_type ==0:
                    top_list=Deal.objects.exclude(deal_type=None).filter(condtion1,cv3=industry.id).values('deal_type').annotate(num_all=Count('id')).order_by('-num_all')[:num]
                else:
                    top_list=Deal.objects.exclude(deal_type=None).filter(condtion1,cv3=industry.id).values('deal_type').annotate(num_all=Sum('amount_usd')).order_by('-num_all')[:num]
    
                for item in top_list:
                    
                    temp_list1[item['deal_type']]=int(item['num_all'])
    except:
        result['error']=ugettext('Something is error!')    

    result['top_list']=temp_list1
    # print(result)

    return HttpResponse(simplejson.dumps(result))



@member_login_required
def ajax_get_list(request,industry_id, country_id, page, pagesize):

    #industry = get_object_or_404(Industry, pk=industry_id)
    #print '*'*80
    #print industry
    #print '*'*80
   
    c = {}
    if page <= 1:
        page = 1
    if pagesize <= 1:
        pagesize = 1
    start_record = (int(page)-1) * int(pagesize)
    end_record = int(start_record) + int(pagesize)
    data = Deal.objects.all()
    if industry_id > 0:
        try:
            industry = Industry.objects.get(pk=industry_id)
            if industry.level == 3:
                data = data.filter(cv3=industry_id)
            elif industry.level == 2:
                data = data.filter(cv2=industry_id)
            else:
                data = data.filter(cv1=industry_id)
        except ObjectDoesNotExist:
            pass
    if int(country_id) > 0:
        data = data.filter(country_id=country_id)
    data = data.order_by("-update_time")[start_record:end_record]
    c['deal_list'] = data
    return render_to_response("deal/"+request.lang+"/ajax_list.html", c, context_instance=RequestContext(request))





