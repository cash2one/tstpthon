from django.shortcuts import render
from django.shortcuts import render,render_to_response, redirect, get_object_or_404, HttpResponse, RequestContext
from django.core.exceptions import ObjectDoesNotExist
from services.models import Member, News,PreferenceKeyword,Country, Industry, Project, Demand, Company, StatusDemand, StatusProject, Preference, Member
from newchama.helper import member_login_required
from services.helper import Helper
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from django.template import loader
from django.contrib import messages
import datetime
import logging
logger = logging.getLogger(__name__)


@member_login_required
def index(request):
    c = {}
    c['title']=_("News List")


    _sql="select tag,max(time) time, max(id) id from cvsource_news where tag <>'' and time <=now() group by tag order by id desc limit 5"

    last5_tag_list=News.objects.raw(_sql)

    news_list=[]
    
    for item in last5_tag_list:
        sub_news_list={}

        main_news=News.objects.filter(tag=item.tag).order_by('-time').first()

        relation_news_list=News.objects.filter(tag=item.tag).order_by('-time')[1:5]

        sub_news_list.update({'main_news':main_news,'relation_news_list':relation_news_list})

        news_list.append(sub_news_list)

    c['news_list'] =news_list

    c['member'] = request.session.get('member', None)

    if c['member']:
        c['preference_list']=PreferenceKeyword.objects.filter(preference__member__id=c['member']['id'],preference__title='news')


    return render_to_response("news/"+request.lang+"/list.html", c, context_instance=RequestContext(request))


@member_login_required
def tag(request,tag):
    c = {}
    c['title']=_("News List")

    news_list=[]
    sub_news_list={}
    main_news=News.objects.filter(tag=tag).order_by('-time').first()
    if main_news:
        relation_news_list=News.objects.filter(tag=tag).order_by('-time')[1:5]
        sub_news_list.update({'main_news':main_news,'relation_news_list':relation_news_list})
        news_list.append(sub_news_list)
        c['news_list'] =news_list

        c['member'] = request.session.get('member', None)

        if c['member']:
            c['preference_list']=PreferenceKeyword.objects.filter(preference__member__id=c['member']['id'],preference__title=Preference().TITLE_PREFERENCE[0][1])

        return render_to_response("news/"+request.lang+"/list.html", c, context_instance=RequestContext(request))
    else:
        return redirect("news.index")

@member_login_required
def detail(request,id):
    c = {}
    c['title']=_("News Detail")
    
    news = get_object_or_404(News, pk=id)
    news.content=news.content.replace(r'src="image/',r'src="http://commons.cvsource.com.cn/UploadImages/news/image/')
    c['news']=news

    c['relation_news']=News.objects.exclude(pk=id).filter(tag=news.tag).order_by('-time')[0:10]

    member_id = request.session.get('member', None)["id"]
    member = Member.objects.get(id=member_id)
    c["is_added_favorite"] = member.is_added_news_to_favorites(news)
    c['member'] = request.session.get('member', None)
    return render_to_response("news/"+request.lang+"/detail.html", c, context_instance=RequestContext(request))


@member_login_required
def search(request):
    c = {}
    is_search = request.GET.get("is_search", "")
    if is_search == '1':
        keyword = request.GET.get("keyword", "")
        if keyword != "":
            news = News.objects.filter(Q(title__contains=keyword) | Q(tag__contains=keyword)).order_by("-time")
            c["keyword"] = keyword
            c["news"] = news[0:10]
            c["total_news"] = news.count()
        c['is_search'] = True
    c['title'] = _("News Search")
    c['member'] = request.session.get('member', None)
    c["countries"] = Helper.find_countries()
    c["industries"] = Helper.find_industries_level1()
    return render_to_response("news/"+request.lang+"/search.html", c, context_instance=RequestContext(request))

@member_login_required
def search_keyword(request):
    c = {}
    c['member'] = request.session.get('member', None)
    member_id = request.session['member']['id']
    member = get_object_or_404(Member,pk=member_id)

    keyword = request.GET.get("keyword", '')
    c["keyword"] = keyword
    news = News.objects.filter(Q(title__contains=keyword) | Q(tag__contains=keyword))
    c['news'] = news.order_by("-time")[0:10]
    c['total_project'] = Project.objects.filter(Q(status=StatusProject.approved) & (Q(name_cn__contains=keyword) | Q(name_en__contains=keyword))).count()
    c['total_demand'] = Demand.objects.filter(Q(status=StatusDemand.approved) & (Q(name_cn__contains=keyword) | Q(name_en__contains=keyword))).count()
    c['total_news'] = news.count()
    #c['total_company'] = Company.objects.filter(Q(short_name_cn__contains=keyword) | Q(short_name_en__contains=keyword)).count()
    #c['total_member'] = Member.objects.filter(Q(last_name__contains=keyword) | Q(first_name__contains=keyword)).count()
    
    write_search_news_log(request,member,keyword)

    return render_to_response("news/"+request.lang+"/search_keyword.html", c, context_instance=RequestContext(request))

@member_login_required
def ajax_search_keyword(request):
    c = {}
    keyword = request.GET.get("keyword", '')
    page = request.GET.get("page", 1)
    pagesize = request.GET.get("pagesize", 10)
    if page <= 1:
        page = 1
    if pagesize <= 1:
        pagesize = 1
    start_record = (int(page)-1) * int(pagesize)
    end_record = int(start_record) + int(pagesize)
    news = News.objects.filter(Q(title__contains=keyword) | Q(tag__contains=keyword))
    c['news'] = news.order_by("-time")[start_record:end_record]
    return render_to_response("news/"+request.lang+"/ajax_search_keyword.html", c, context_instance=RequestContext(request))