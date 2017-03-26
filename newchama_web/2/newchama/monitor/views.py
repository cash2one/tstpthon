#encoding:utf-8
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from industry.models import Industry
from monitor.models import ShanghaiShenzhenNotice, HkNotice, DailyDeal
from forms import NoticeForm
from utils import export_daily_deals, read_filter_file
import operator
from django.db.models import Q
import datetime
from collections import namedtuple
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

today_start = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
today_end = datetime.datetime.combine(datetime.date.today(), datetime.time.max)


def hk_notice_content(request, id):
    c = {}
    notice = HkNotice.objects.get(pk=id)
    if notice:
        form = NoticeForm({'content':notice.content})
        c['form'] = form
    return render(request, 'monitor/notice_content.html', c)


def notice_content(request, id):
    c = {}
    notice = ShanghaiShenzhenNotice.objects.get(pk=id)
    if notice:
        form = NoticeForm({'content':notice.body})
        c['form'] = form
    return render(request, 'monitor/notice_content.html', c)


def daily_notices(request):
    c = {}
    c['start_time'] = today_start
    c['end_time'] = today_end
    c['industries'] = Industry.objects.filter(level=1, is_display=True)
    return render(request, 'monitor/daily_notices.html', c)


def deals_query(request):
    c = {}
    start_time = request.GET.get("deal_start_time", today_start)
    end_time = request.GET.get("deal_end_time", today_end)

    if not isinstance(start_time, datetime.datetime):
        start_date = datetime.datetime.strptime(start_time, '%m/%d/%Y')
        start_time = datetime.datetime.combine(start_date, datetime.time.min)
    if not isinstance(end_time, datetime.datetime):
        end_date = datetime.datetime.strptime(end_time, '%m/%d/%Y')
        end_time = datetime.datetime.combine(end_date, datetime.time.max)

    c['daily_deals'] = DailyDeal.objects.filter(date__range=(start_time, end_time))

    return render(request, 'monitor/deals_query.html', c)


def notices_query(request):
    c = {}
    start_time = request.GET.get("start_time", today_start)
    end_time = request.GET.get("end_time", today_end)

    if not isinstance(start_time, datetime.datetime):
        start_date = datetime.datetime.strptime(start_time, '%m/%d/%Y')
        start_time = datetime.datetime.combine(start_date, datetime.time.min)
    if not isinstance(end_time, datetime.datetime):
        end_date = datetime.datetime.strptime(end_time, '%m/%d/%Y')
        end_time = datetime.datetime.combine(end_date, datetime.time.max)

    # django timezone issue: automatically deduct 8 hours when querying
    # django timezone issue: automatically add 8 hours when add time using save()
    start_time += datetime.timedelta(hours=8)
    end_time += datetime.timedelta(hours=8)

    # shsz notice query
    exclude_keywords = read_filter_file('shsz_notice_no_keywords.txt')
    shsz_stock_list = read_filter_file('shsz_stock_list.txt')
    keywords = read_filter_file('shsz_notice_keywords.txt')

    include_query = reduce(operator.or_, (Q(title__contains=item) for item in keywords))
    exclude_query = reduce(operator.or_, (Q(title__contains=item) for item in exclude_keywords))

    shsz_notices = ShanghaiShenzhenNotice.objects.filter(published_date__range=(start_time, end_time)).values('id', 'market_type__market_name', 'symbol', 'company', 'title', 'notice_type__type_name', 'published_date', 'pdf_url')
    shsz_notices = shsz_notices.filter(symbol__in=shsz_stock_list).filter(include_query)
    shsz_notices = shsz_notices.exclude(exclude_query)
    notices_ids = [notice['id'] for notice in shsz_notices]
    notices_contents = ShanghaiShenzhenNotice.objects.filter(id__in=notices_ids).values('body')
    c['shsz_notices'] = zip(shsz_notices, notices_contents)

    # hk notice query
    hk_stock_list = read_filter_file('hk_stock_list.txt')
    hk_notice_types = read_filter_file('hk_notice_types.txt', return_type='int')
    hk_notices = HkNotice.objects.filter(time__range=(start_time, end_time)).values('id', 'time', 'symbol', 'stock_name', 'title', 'url')
    hk_notices = hk_notices.filter(symbol__in=hk_stock_list).filter(types__in=hk_notice_types)
    hk_notices_ids = [notice['id'] for notice in hk_notices]
    contents_types = HkNotice.objects.filter(id__in=hk_notices_ids)
    c['hk_notices'] = zip(hk_notices, contents_types)
    return render(request, 'monitor/notices_query.html', c)


@csrf_exempt
def export_to_xls(request):
    id_lst = request.POST.getlist('check_deals')
    workbook = export_daily_deals(id_lst)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="export.xls"'
    workbook.save(response)
    return response


@csrf_exempt
def submit_deals_to_database(request):
    """
        Declarartion: fields in js
        fields = ('stock_code',
                  'company_short_name',
                  'date',
                  'industry_1',
                  'industry_2',
                  'company_full_name',
                  'target_firm',
                  'transaction_type',
                  'transaction_currency',
                  'transaction_amount',
                  'transaction_ratio',
                  'content',
                  'pdf_url')
    """
    Record = namedtuple('Record', request.POST.keys())
    # Todo why len is  1, figure it out
    #print 'len', len([Record(*t) for t in zip(*(request.POST.getlist(k) for k in request.POST.keys()))])
    #for record in [Record(*t) for t in zip(*(request.POST.getlist(k) for k in request.POST.keys()))]:
    for record in list(map(Record, *(request.POST.getlist(k) for k in request.POST.keys()))):
        daily_deal = DailyDeal(
            company_short_name=record.company_short_name,
            stock_symbol=record.stock_code,
            cv1=Industry.objects.get(pk=record.industry_1),
            cv2=Industry.objects.get(pk=record.industry_2),
            company_full_name=record.company_full_name,
            target_company=record.target_firm,
            deal_type=record.transaction_type,
            deal_currency=record.transaction_currency,
            deal_amount= None if record.transaction_amount == u"" else record.transaction_amount,
            deal_ratio=None if record.transaction_ratio == u"" else record.transaction_ratio,
            deal_content=record.content,
            date=datetime.datetime.strptime(record.date, '%Y-%m-%d'),
            published_date=datetime.datetime.strptime(record.published_date, '%m/%d/%Y'),
            financial_advisor=record.financial_advisor,
            target_company_tags=record.target_company_tags,
            investor_tags=record.investor_tags
        )
        daily_deal.save()
    return redirect("monitor.daily_notices")

