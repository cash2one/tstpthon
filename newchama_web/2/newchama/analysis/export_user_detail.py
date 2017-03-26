#encoding:utf-8
import calendar
from decimal import Decimal
import os, sys, datetime, time, random, xlwt, logging, traceback

sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/adminnewchama/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from project.models import Project, Country, StatusProject
from subscribe.models import Subscribe, SubscribeKeyword, SubscribeSendRecord
from django.utils import simplejson
from django.template import Context
from demand.models import Demand
from industry.models import Industry
from member.models import Member, CompanyInvestmentField
from member_message.models import Message, Favorites
from log.models import Log
from newchama.decorators import login_required, permission_required
from recommond.models import ProjectTargetCompanyDetail
from django.shortcuts import render_to_response, RequestContext
from collections import namedtuple

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.ERROR,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='user_detail_error.log',
                filemode='a')

export_path = "/var/www/newchama_media/userdetail/"

def run_detail(starttime, endtime):
    try:
        encoded = "utf-8"
        # starttime = '2015-05-01'
        # endtime= '2015-05-31'
        member = Member.objects.exclude(first_name=None, last_name=None).order_by('first_name')
        # member = Member.objects.filter(id__lte=2)
        if member:
            wbk = xlwt.Workbook()
            for m in member:
                if m.first_name or m.last_name:
                    ws = wbk.add_sheet(m.__unicode__().decode(encoded), cell_overwrite_ok=True)
                    sheetX = 0
                    ws.write(1, sheetX, m.__unicode__())
                    ws.write(2, sheetX, m.email)
                    #login
                    sheetX += 1
                    ws.write(0, sheetX, u'登录')
                    logs = Log.objects.filter(time__gte=starttime, time__lte=endtime, operation_type=1, target_type=1, user=m)
                    if logs:
                        i = 0
                        # for i, l in enumerate(logs):
                        for l in logs:
                            i += 1
                            ws.write(i, sheetX, datetime.datetime.strftime(l.time, '%Y-%m-%d %H:%M:%S'))

                    #view project
                    sheetX += 1
                    ws.write(0, sheetX, u'项目浏览')
                    logs = Log.objects.filter(time__gte=starttime, time__lte=endtime, operation_type=2, target_type=2, user=m)
                    if logs:
                        i = 0
                        # for i, l in enumerate(logs):
                        for l in logs:
                            i += 1
                            ws.write(i, sheetX, datetime.datetime.strftime(l.time, '%Y-%m-%d %H:%M:%S'))

                    #view demand
                    sheetX += 1
                    ws.write(0, sheetX, u'需求浏览')
                    logs = Log.objects.filter(time__gte=starttime, time__lte=endtime, operation_type=2, target_type=3, user=m)
                    if logs:
                        i = 0
                        # for i, l in enumerate(logs):
                        for l in logs:
                            i += 1
                            ws.write(i, sheetX, datetime.datetime.strftime(l.time, '%Y-%m-%d %H:%M:%S'))

                    #send message
                    sheetX += 1
                    ws.write(0, sheetX, u'发送消息')
                    datas = Message.objects.filter(add_time__gte=starttime, add_time__lte=endtime, sender=m)
                    if datas:
                        i = 0
                        # for i, l in enumerate(logs):
                        for d in datas:
                            i += 1
                            ws.write(i, sheetX, datetime.datetime.strftime(d.add_time, '%Y-%m-%d %H:%M:%S'))

                    #publish project
                    sheetX += 1
                    ws.write(0, sheetX, u'项目发布')
                    datas = Project.objects.filter(add_time__gte=starttime, add_time__lte=endtime, member=m, status=2)
                    if datas:
                        i = 0
                        # for i, l in enumerate(logs):
                        for d in datas:
                            i += 1
                            ws.write(i, sheetX, datetime.datetime.strftime(d.add_time, '%Y-%m-%d %H:%M:%S'))

                    #publish demand
                    sheetX += 1
                    ws.write(0, sheetX, u'需求发布')
                    datas = Demand.objects.filter(add_time__gte=starttime, add_time__lte=endtime, member=m, status=2)
                    if datas:
                        i = 0
                        # for i, l in enumerate(logs):
                        for d in datas:
                            i += 1
                            ws.write(i, sheetX, datetime.datetime.strftime(d.add_time, '%Y-%m-%d %H:%M:%S'))

                    #favorite project
                    sheetX += 1
                    ws.write(0, sheetX, u'项目收藏')
                    datas = Favorites.objects.filter(add_time__gte=starttime, add_time__lte=endtime, type_relation=1, member=m)
                    if datas:
                        i = 0
                        # for i, l in enumerate(logs):
                        for d in datas:
                            i += 1
                            ws.write(i, sheetX, datetime.datetime.strftime(d.add_time, '%Y-%m-%d %H:%M:%S'))

                    #favorite demand
                    sheetX += 1
                    ws.write(0, sheetX, u'需求收藏')
                    datas = Favorites.objects.filter(add_time__gte=starttime, add_time__lte=endtime, type_relation=2, member=m)
                    if datas:
                        i = 0
                        # for i, l in enumerate(logs):
                        for d in datas:
                            i += 1
                            ws.write(i, sheetX, datetime.datetime.strftime(d.add_time, '%Y-%m-%d %H:%M:%S'))
            random_no = str(random.randint(0, 999999)).zfill(6)
            wbk.save(export_path + "detail_"+ random_no +".xls")
    except Exception, e:
        print e
        logging.error(e)


def run_count(starttime, endtime):
    try:
        encoded = "utf-8"
        member = Member.objects.exclude(first_name=None, last_name=None).order_by('first_name')
        # member = Member.objects.filter(id__lte=2)
        if member:
            wbk = xlwt.Workbook()
            ws = wbk.add_sheet(u'用户活跃度统计', cell_overwrite_ok=True)
            sheetX = 0
            sheetY = 0
            ws.write(sheetY, sheetX, u'用户')
            sheetX += 1
            ws.write(sheetY, sheetX, u'项目浏览')
            sheetX += 1
            ws.write(sheetY, sheetX, u'需求浏览')
            sheetX += 1
            ws.write(sheetY, sheetX, u'发送消息')
            sheetX += 1
            ws.write(sheetY, sheetX, u'项目发布')
            sheetX += 1
            ws.write(sheetY, sheetX, u'需求发布')
            sheetX += 1
            ws.write(sheetY, sheetX, u'项目收藏')
            sheetX += 1
            ws.write(sheetY, sheetX, u'需求收藏')
            for m in member:
                if m.first_name or m.last_name:
                    #login
                    # sheetX += 1
                    # ws.write(0, sheetX, u'登录')
                    # logs = Log.objects.filter(time__gte=starttime, time__lte=endtime, operation_type=1, target_type=1, user=m)

                    #view project
                    view_project_count = Log.objects.filter(time__gte=starttime, time__lte=endtime, operation_type=2, target_type=2, user=m).count()

                    #view demand
                    view_demand_count = Log.objects.filter(time__gte=starttime, time__lte=endtime, operation_type=2, target_type=3, user=m).count()

                    #send message
                    send_message_count = Message.objects.filter(add_time__gte=starttime, add_time__lte=endtime, sender=m).count()

                    #publish project
                    publish_project_count = Project.objects.filter(add_time__gte=starttime, add_time__lte=endtime, member=m, status=2).count()

                    #publish demand
                    publish_demand_count = Demand.objects.filter(add_time__gte=starttime, add_time__lte=endtime, member=m, status=2).count()

                    #favorite project
                    favorite_project_count = Favorites.objects.filter(add_time__gte=starttime, add_time__lte=endtime, type_relation=1, member=m).count()

                    #favorite demand
                    favorite_demand_count = Favorites.objects.filter(add_time__gte=starttime, add_time__lte=endtime, type_relation=2, member=m).count()

                    if view_project_count > 0 or view_demand_count > 0 or send_message_count > 0 or publish_project_count > 0 or publish_demand_count > 0 or favorite_project_count > 0 or favorite_demand_count > 0:
                        sheetX = 0
                        sheetY += 1
                        ws.write(sheetY, sheetX, m.email)
                        sheetX += 1
                        ws.write(sheetY, sheetX, view_project_count)
                        sheetX += 1
                        ws.write(sheetY, sheetX, view_demand_count)
                        sheetX += 1
                        ws.write(sheetY, sheetX, send_message_count)
                        sheetX += 1
                        ws.write(sheetY, sheetX, publish_project_count)
                        sheetX += 1
                        ws.write(sheetY, sheetX, publish_demand_count)
                        sheetX += 1
                        ws.write(sheetY, sheetX, favorite_project_count)
                        sheetX += 1
                        ws.write(sheetY, sheetX, favorite_demand_count)

            random_name = export_path + "total_"+ str(random.randint(0, 999999)).zfill(6) +".xls"
            wbk.save(random_name)
            print "export successfully , path: " + random_name
    except Exception, e:
        print e
        logging.error(e)


'''
    defaut date is 'yyyy-mm'
    stay_login_rate
'''
def stay_login_rate(starttime, endtime):
    #search user before starttime a month
    running = True
    et = endtime.split("-")
    finish_starttime = get_firstday_of_month(et[0], et[1])
    datas = []
    while running:
        st = starttime.split("-")
        this_st = get_firstday_of_month(st[0], st[1])
        this_et = get_lastday_of_month(st[0], st[1])
        before_time = minusMonByMon(this_st)
        bt = before_time.split("-")
        before_st = get_firstday_of_month(bt[0], int(bt[1]))
        before_et = get_lastday_of_month(bt[0], int(bt[1]))
        #add_time__gte=before_st,
        members = Member.objects.filter(add_time__lte=before_et).order_by("first_name").exclude(company_id=27)         #exclude the company is dami capital
        active_num = 0
        if members:
            for m in members:
                bool = find_member_active(this_st, this_et, m.id)
                if bool:
                    active_num += 1
                # ms.append(m.id)
            # login_count = Log.objects.filter(time__gte=this_st, time__lte=this_et, operation_type=1, target_type=1, user__in=ms).values("user").distinct().count()
            # print "curr starttime is '" + this_st + "' endtime is '" + this_et + "', total register user is " + str(len(members))  + " until last month login user " + str(login_count)
            result = 0
            if len(members) > 0:
                result = round(active_num / float(len(members)), 4) * 100
            ret = []
            ret.append(get_year_month(this_st))
            ret.append(result)
            ret.append(active_num)
            ret.append(len(members))
            datas.append(ret)
        if finish_starttime == this_st:
            running = False
        else:
            starttime = addMonByMon(this_st)

    return datas


'''
    current month register and user active
'''
def curr_month_active(starttime, endtime):
    running = True
    et = endtime.split("-")
    finish_starttime = get_firstday_of_month(et[0], et[1])
    datas = []
    while running:
        st = starttime.split("-")
        this_st = get_firstday_of_month(st[0], st[1])
        this_et = get_lastday_of_month(st[0], st[1])
        print "this_st = " + this_st + " end time = " + this_et
        members = Member.objects.filter(add_time__gte=this_st, add_time__lte=this_et).order_by("first_name").exclude(company_id=27)         #exclude the company is dami capital
        result = 0
        active_num = 0
        if members:
            for m in members:
                bool = find_member_active(this_st, this_et, m.id)
                if bool:
                    active_num += 1
            # print "curr starttime is '" + this_st + "' endtime is '" + this_et + "', total register user is " + str(len(members)) + " active user count " + str(active_num)
            if len(members) > 0:
                result = round(active_num / float(len(members)), 4) * 100
        ret = []
        ret.append(get_year_month(this_st))
        ret.append(result)
        ret.append(active_num)
        ret.append(len(members))
        datas.append(ret)
        if finish_starttime == this_st:
            running = False
        else:
            starttime = addMonByMon(this_st)
    return datas


'''
    current month register and user active
'''
def every_month_active(starttime, endtime):
    running = True
    et = endtime.split("-")
    finish_starttime = get_firstday_of_month(et[0], et[1])
    st = starttime.split("-")
    start_time = get_firstday_of_month(st[0], st[1])
    datas = []
    while running:
        result = 0
        active_num = 0
        st = starttime.split("-")
        this_st = get_firstday_of_month(st[0], st[1])
        this_et = get_lastday_of_month(st[0], st[1])
        before_time = minusMonByMon(this_st)
        member_total, active_num = find_active_user(start_time, this_et)
        if member_total > 0:
            result = round(active_num / float(member_total), 4) * 100
        ret = []
        ret.append(get_year_month(this_st))
        ret.append(result)
        ret.append(active_num)
        ret.append(member_total)
        datas.append(ret)
        if finish_starttime == this_st:
            running = False
        else:
            starttime = addMonByMon(this_st)
    return datas


def find_active_user(start_time, end_time):
    currtime = start_time
    members = Member.objects.filter(add_time__lte=end_time).order_by("first_name").exclude(company_id=27)         #exclude the company is dami capital
    active_num = 0
    if members:
        for m in members:
            starttime = currtime
            bool = True
            running = True
            while running:
                st = starttime.split("-")
                this_st = get_firstday_of_month(st[0], st[1])
                this_et = get_lastday_of_month(st[0], st[1])
                #add_time__gte=before_st,
                if members:
                    bool = find_member_active(this_st, this_et, m.id)
                    if bool is False:
                        break

                if str(end_time) == this_et:
                    running = False
                else:
                    starttime = addMonByMon(this_st)
            if bool:
                active_num += 1
    return len(members), active_num


'''
    total register and active
'''
def total_active():
    result = 0
    active_num = 0
    members = Member.objects.order_by("first_name").exclude(company_id=27)         #exclude the company is dami capital
    if members:
        for m in members:
            bool = find_member_active(None, None, m.id)
            if bool:
                active_num += 1
        print "total register user is " + str(len(members)) + " active user count " + str(active_num)
        if len(members) > 0:
            result = round(active_num / float(len(members)), 4) * 100
    ret = []
    ret.append(result)
    ret.append(active_num)
    ret.append(len(members))
    return ret


'''
find member active
if isLogin then only check user is login return true else return false
if isLogin is False then
    if view_project_count > 0 or view_demand_count > 0 or send_message_count > 0 or publish_project_count > 0
        or publish_demand_count > 0 or favorite_project_count > 0 or favorite_demand_count > 0
        return True
else return false
'''
def find_member_active(starttime, endtime, member_id):
    #login time
    # login_count = Log.objects.filter(time__gte=starttime, time__lte=endtime, operation_type=1, target_type=1, user__in=member).count()
    # if login_count > 0:
    #     return True
    #view project
    view_project_count = count_view_project(starttime, endtime, member_id)

    #view demand
    view_demand_count = count_view_demand(starttime, endtime, member_id)

    #favorite project
    favorite_project_count = count_favorite_project(starttime, endtime, member_id)

    #favorite demand
    favorite_demand_count = count_favorite_demand(starttime, endtime, member_id)

    #publish project
    publish_project_count = count_publish_project(starttime, endtime, member_id)

    #publish demand
    publish_demand_count = count_publish_demand(starttime, endtime, member_id)

    #send message
    send_message_count = count_message(starttime, endtime, member_id)

    if view_project_count > 0 or view_demand_count > 0 or send_message_count > 0 or publish_project_count > 0 or publish_demand_count > 0 or favorite_project_count > 0 or favorite_demand_count > 0:
        return True

    return False


def count_view_project(starttime, endtime, member_id):
    #view project
    view_project = Log.objects.filter(operation_type=2, target_type=2, user_id=member_id)
    if starttime:
        view_project = view_project.filter(time__gte=starttime, time__lte=endtime)
    return view_project.count()


def count_view_demand(starttime, endtime, member_id):
    #view demand
    view_demand = Log.objects.filter(operation_type=2, target_type=3, user_id=member_id)
    if starttime:
        view_demand = view_demand.filter(time__gte=starttime, time__lte=endtime)
    return view_demand.count()


def count_favorite_project(starttime, endtime, member_id):
    favorite_project = Favorites.objects.filter(type_relation=1, member_id=member_id)
    if starttime:
        favorite_project = favorite_project.filter(add_time__gte=starttime, add_time__lte=endtime, )
    return favorite_project.count()


def count_favorite_demand(starttime, endtime, member_id):
    favorite_demand = Favorites.objects.filter(type_relation=2, member_id=member_id)
    if starttime:
        favorite_demand = favorite_demand.filter(add_time__gte=starttime, add_time__lte=endtime, )
    return favorite_demand.count()


def count_message(starttime, endtime, member_id):
    send_message = Message.objects.filter(sender_id=member_id)
    if starttime:
        send_message = send_message.filter(add_time__gte=starttime, add_time__lte=endtime, )
    return send_message.count()


def count_publish_project(starttime, endtime, member_id):
    publish_project = Project.objects.filter(member_id=member_id).exclude(status=5)
    if starttime:
        publish_project = publish_project.filter(add_time__gte=starttime, add_time__lte=endtime, )
    return publish_project.count()


def count_publish_demand(starttime, endtime, member_id):
    publish_demand = Demand.objects.filter(member_id=member_id).exclude(status=5)
    if starttime:
        publish_demand = publish_demand.filter(add_time__gte=starttime, add_time__lte=endtime, )
    return publish_demand.count()


def count_push_project(starttime, endtime, member_id):
    push_project = ProjectTargetCompanyDetail.objects.filter(member_id=member_id)
    if starttime:
        push_project = push_project.filter(add_time__gte=starttime, add_time__lte=endtime, )
    return push_project.count()


def count_match_project(starttime, endtime, member_id):
    return 0;


def count_match_demand(starttime, endtime, member_id):
    return 0;


def weekbegend(year, week):
    """
    Calcul du premier et du dernier jour de la semaine ISO
    """
    d = datetime.date(year, 1, 1)
    delta_days = d.isoweekday() - 1
    delta_weeks = week
    if year == d.isocalendar()[0]:
        delta_weeks -= 1
    # delta for the beginning of the week
    delta = datetime.timedelta(days=-delta_days, weeks=delta_weeks)
    weekbeg = d + delta
    # delta2 for the end of the week
    delta2 = datetime.timedelta(days=6-delta_days, weeks=delta_weeks)
    weekend = d + delta2
    return weekbeg, weekend


def getWeeklys(d1, d2):
    # d2 = datetime.date(2015,05,01)
    # d1 = datetime.date(2015,05,31)
    diff = (d1 - d2).days
    i = 0
    weeklys = []
    weeklyInfo = namedtuple("weeklyInfo", ["currWeekly", "startDate", "endDate"])
    while i < diff:
        i += 1
        aDay = datetime.timedelta(days=1)
        d2 = d2 + aDay
        currWeek = int(d2.strftime("%W")) + 1
        startdate, enddate = weekbegend(d2.year, currWeek)
        wi = weeklyInfo(currWeek, datetime.datetime.strftime(startdate, '%Y-%m-%d'), datetime.datetime.strftime(enddate, '%Y-%m-%d'))
        if not wi in weeklys:
            weeklys.append(wi)
        # d2 = enddate
    return weeklys


def stay_login_rate_redesign():
    months_ids = []
    curr_year = datetime.datetime.now().year

    for month in range(1, 6):
        start_date = datetime.date(curr_year, month, 1)
        if month == 12:
            end_date = datetime.date(curr_year, 12, 31)
        else:
            end_date = datetime.date(curr_year, month+1, 1)
        members = Member.objects.filter(add_time__range=(start_date, end_date)).order_by("first_name").exclude(company_id=27)
        months_ids.append(members)

    total_weeks = datetime.date(curr_year, 12, 31).isocalendar()[1]

    first_day_of_year = datetime.date(curr_year, 1, 1)
    res = []  #  52 or 53 weeks  *  12 month(list)
    for week in range(1, 22+1):
        weeks_months = [] # row
        for month in range(0, 5):
            start_date_of_week, end_date_of_week = weekbegend(curr_year, week)
            if month < start_date_of_week.month:
                if months_ids[month]:
                    active_num = 0
                    for m in months_ids[month]:
                        bool = find_member_active(start_date_of_week, end_date_of_week, m.id)
                        if bool:
                            active_num += 1
                        # print  ">>>>>>>>>>>>>>>>>>>>>>>>>>>member_id = " + str(m.id) + " active_num = " + str(active_num) + " bool = " + str(bool) + " start_date_of_week = " + str(start_date_of_week) + " end_date_of_week = " + str(end_date_of_week)
                    result = 0
                    # print  " curr_month = " + str(month) + " month_total_register = " + str(len(months_ids[month])) + " active_num = " + str(active_num) + "; detail_member = " + str(months_ids[month])
                    if len(months_ids[month]) > 0:
                        result = round(active_num / float(len(months_ids[month])), 4) * 100
                    weeks_months.append(result)
                    result = 0
            else:
                weeks_months.append(0)
        res.append(weeks_months) # append row
    return res, months_ids


def get_year_month(date):
    ds = date.split("-")
    arr = (ds[0], ds[1])
    return "-".join("%s" %i for i in arr)


'''
get the first day of month
date format = "YYYY-MM-DD"
'''
def get_firstday_of_month(year, mon):
    days="01"
    if(int(mon)<10):
        mon = "0"+str(int(mon))
    arr = (year, mon, days)
    return "-".join("%s" %i for i in arr)


'''
get the last day of month
date format = "YYYY-MM-DD"
'''
def get_lastday_of_month(year, mon):
    days=calendar.monthrange(int(year), int(mon))[1]
    mon = addzero(mon)
    '''
    for django change, because django use usa time, when django find this is chinese time,
    then django will minus 8 hours automatically, so if the last date is '2015-3-31' then it will changed '2015-3-30 16:00:00',
    because django suggest the  '2015-3-31' is  '2015-3-31 00:00:00' so the result is  '2015-3-30 16:00:00'.
    and we need add one more day to fixed it.
    '''
    dat = str(year) + "-" + str(mon) + "-" + str(days)
    _time = datetime.datetime.strptime(dat, '%Y-%m-%d')
    _time = _time + datetime.timedelta(days=1)
    return datetime.datetime.strftime(_time, '%Y-%m-%d')
    '''
    fixed end
    '''
    # arr = (year, mon, days)
    # return "-".join("%s" %i for i in arr)


'''''
add 0 before 0-9
return 01-09
'''
def addzero(n):
    nabs = abs(int(n))
    if(nabs<10):
        return "0"+str(nabs)
    else:
        return str(nabs)


def addMonByMon(_time):
    _time_arr = _time.split('-')
    _tyears = int(_time_arr[0])
    _tmonth = int(_time_arr[1]) + 1

    if _tmonth==13:
        _tmonth = 1
        _tyears = _tyears + 1
    return str(_tyears) + '-'+addzero(_tmonth) + '-'+addzero(_time_arr[2])


def minusMonByMon(_time):
    _time_arr = _time.split('-')
    _tyears = int(_time_arr[0])
    _tmonth = int(_time_arr[1]) - 1

    if _tmonth==0:
        _tmonth = _tmonth + 12
        _tyears = _tyears - 1
    return str(_tyears)+'-'+addzero(_tmonth)+'-'+addzero(_time_arr[2])


@login_required
@permission_required("analysis")
def index(request):
    c={}
    starttime = request.GET.get("starttime", "2015-05-01")
    endtime = request.GET.get("endtime", "2015-05-31")
    if starttime:
        c['stayRate'] = stay_login_rate(starttime, endtime)

        c['currActive'] = curr_month_active(starttime, endtime)

        c['everyActive'] = every_month_active(starttime, endtime)

        c['totalActive'] = total_active()

    c["starttime"] = starttime
    c["endtime"] = endtime

    return render_to_response("analysis/user_detail_dim.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def weekly_active_detail(request):
    c = {}
    d1 = datetime.datetime.now()
    d3 = d1 + datetime.timedelta(days = -7)
    d2 = d1 + datetime.timedelta(days = -6)
    starttime = request.GET.get("starttime", datetime.datetime.strftime(d3, '%Y-%m-%d'))
    endtime = request.GET.get("endtime", datetime.datetime.strftime(d2, '%Y-%m-%d'))

    if starttime:
        d2 = datetime.datetime.strptime(starttime,'%Y-%m-%d').date()
        d1 = datetime.datetime.strptime(endtime,'%Y-%m-%d').date()
        weeklys = getWeeklys(d1, d2)
        weekly4Member = groupMemberAction(weeklys)
        # print str(weekly4Member)
        result = []

        # 0:member_id", "1:view_project", "2:view_demand", "3:favorite_project", "4:favorite_demand", "5:publish_project", "6:publish_demand", "7:match_project", "8:match_demand", "9:push_project", "10:send_message"
        #周活跃度
        result.append(countActiveMember("周活跃度", weekly4Member, ["view_project", "view_demand", "favorite_project", "favorite_demand", "publish_project", "publish_demand", "push_project", "send_message"]))
        #轻度活跃
        result.append(countActiveMember("轻度活跃", weekly4Member, ["view_project", "view_demand", "favorite_project", "favorite_demand"]))
        #浏览
        result.append(countActiveMember("浏览", weekly4Member, ["view_project", "view_demand"]))
        #收藏
        result.append(countActiveMember("收藏", weekly4Member, ["favorite_project", "favorite_demand"]))
        #重度活跃
        result.append(countActiveMember("重度活跃", weekly4Member, ["publish_project", "publish_demand", "push_project", "send_message"]))
        #发布
        result.append(countActiveMember("发布", weekly4Member, ["publish_project", "publish_demand"]))
        #匹配
        result.append(countActiveMember("匹配", weekly4Member, ["match_project", "match_demand"]))
        #推送
        result.append(countActiveMember("推送", weekly4Member, ["push_project"]))
        #私信
        result.append(countActiveMember("私信", weekly4Member, ["send_message"]))

    c["starttime"] = starttime
    c["endtime"] = endtime
    c["weekly"] = weeklys
    c["result"] = result
    return render_to_response("analysis/user_weekly_active_detail.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("analysis")
def weekly_active(request):
    result, months = stay_login_rate_redesign()
    c = {}
    c["result"] = result
    c["months"] = months
    return render_to_response("analysis/user_weekly_active.html", c, context_instance=RequestContext(request))


def exportIndustryAndKeyword_Company():
    cifs = CompanyInvestmentField.objects.all()[:10]
    industrys = []
    keywords = []
    if cifs:
        for c in cifs:
            tags = c.tags
            if tags:
                tempi, tempk = analysisIndustry(tags)
                if tempi:
                    for t in tempi:
                        i = checkIsExsitInIndustrys(industrys, t)
                        # if i > -1:
                        #     exsitKey = keywords[i]
                        #     if len(exsitKey) > 0:
                        #         exsitKey = exsitKey + "," + tempk
                        #     else:
                        #         exsitKey = tempk
                        #     distinctKey = deleteDulpe(exsitKey)
                        #     keywords[i] = distinctKey
                        # else:
                        #     industrys.append(t)
                        #     keywords.append(tempk)

                        if i > -1:
                            exsitKey = keywords[i]
                            if len(exsitKey) > 0:
                                tempk = exsitKey + "," + tempk
                            keywords[i] = deleteDulpe(tempk)
                        else:
                            industrys.append(t)
                            keywords.append(tempk)


    return industrys, keywords


def deleteDulpe(tempk):
    if tempk:
        tks = tempk.split(",")
        tk = set(tks)
        return ",".join(tk)
    return ""


def checkIsExsitInIndustrys(industrys, tempi):
    for i, k in enumerate(industrys):
        if k == tempi:
            return i
    return -1


def analysisIndustry(keywords):
    ks = keywords.split(",")
    industry = []
    keyword = []
    for k in ks:
        ind = None
        inds = Industry.objects.filter(name_cn=k)
        if inds:
            ind = inds[0]
        if ind:
            industry.append(handleIndustryLevel(ind))
        else:
            keyword.append(k)
    return industry, ",".join(keyword)


def exportIndustryAndKeyword_Project():
    industrys = []
    keywords = []
    projects = Project.objects.filter(status=2).order_by("-id")[:10]
    if projects:
        for p in projects:
            ind = p.company_industry
            if ind:
                industry = handleIndustryLevel(ind)

                mks = p.project_keyword.all()
                keys = ""
                if len(mks) > 0:
                    for k in mks:
                        keys += k.keyword + ","

                mks = p.project_keyword_en.all()
                if len(mks) > 0:
                    for k in mks:
                        keys += k.keyword + ","

                mks = p.project_keyword_admin.all()
                if len(mks) > 0:
                    for k in mks:
                        keys += k.keyword + ","

                if len(keys) > 0:
                    keys = keys[0 : len(keys) - 1]

                i = checkIsExsitInIndustrys(industrys, industry)
                if i > -1:
                    exsitKey = keywords[i]
                    if len(exsitKey) > 0:
                        keys = exsitKey + "," + keys
                    keywords[i] = deleteDulpe(keys)
                else:
                    industrys.append(industry)
                    keywords.append(keys)

    return industrys, keywords


def handleIndustryLevel(ind):
    industry = []
    if ind.level == 3:
        industry = ind.father.father.name_cn + "," + ind.father.name_cn + "," + ind.name_cn
    elif ind.level == 2:
        industry = ind.father.name_cn + "," + ind.name_cn + ","
    else:
        industry = ind.name_cn + ",,"
    return industry


def findIndustryAndKeyword():

    print "start loop project"
    industrys, keywords = exportIndustryAndKeyword_Project()
    # for i, k in zip(industrys, keywords):
    #     print str(i) + " keywords = " + str(k)
    print "end loop project"
    print "start loop company"
    industrys_i, keywords_i = exportIndustryAndKeyword_Company()
    print "end loop company"
    # for i, k in zip(industrys_i, keywords_i):
    #     print str(i) + " keywords = " + str(k)
    # if True:
    #     return
    print "start loop project in result"

    industry_result = []
    keyword_result = []
    for i, industry in enumerate(industrys):
        keys_i = keywords[i]
        for k, industry_i in enumerate(industrys_i):
            if industry == industry_i:
                if len(keys_i) > 0:
                    keys_i = keys_i + "," + keywords_i[k]
                else:
                    keys_i = keywords_i[k]
                break
        tks = keys_i.split(",")
        tk = set(tks)
        industry_result.append(industry)
        keyword_result.append(",".join(tk))
    print "end loop project in result"

    print "start loop compnay in result"
    industry_result_2 = industry_result
    keyword_result_2 = keyword_result
    for i, industry in enumerate(industrys_i):
        keys_i = keywords_i[i]
        # print industry + "   keyword = " + keys_i
        for k, industry_r in enumerate(industry_result_2):
            if industry == industry_r:
                if len(keys_i) > 0:
                    keys_i = keys_i + "," + keyword_result_2[k]
                else:
                    keys_i = keyword_result_2[k]
        i = checkIsExsitInIndustrys(industry_result, industry)
        if i > -1:
            exsitKey = keyword_result[i]
            if len(exsitKey) > 0:
                keys_i = keys_i + "," + exsitKey
            keyword_result[i] = deleteDulpe(keys_i)
        else:
            industry_result.append(industry)
            keyword_result.append(deleteDulpe(keys_i))
    print "end loop project in result"

    if industry_result:
        strs, count_nums = getTotalKeywords(keyword_result)
        wbk = xlwt.Workbook()
        ws = wbk.add_sheet(u'用户活跃度统计', cell_overwrite_ok=True)
        sheetX = 0
        sheetY = 0
        ws.write(sheetY, sheetX, u'一级行业')
        sheetX += 1
        ws.write(sheetY, sheetX, u'二级行业')
        sheetX += 1
        ws.write(sheetY, sheetX, u'三级行业')
        sheetX += 1
        ws.write(sheetY, sheetX, u'关键字')
        for i, k in zip(industry_result, keyword_result):
            sheetX = 0
            sheetY += 1
            industry_r = i.split(",")
            ws.write(sheetY, sheetX, industry_r[0])
            sheetX += 1
            ws.write(sheetY, sheetX, industry_r[1])
            sheetX += 1
            ws.write(sheetY, sheetX, industry_r[2])
            sheetX += 1
            count_nums, k = isMaxThen(strs, k, count_nums, 2)
            ws.write(sheetY, sheetX, k)
        random_name = export_path + "industry_keyword_"+ str(random.randint(0, 999999)).zfill(6) +".xls"
        wbk.save(random_name)
        print "export successfully , path: " + random_name


def getTotalKeywords(keyword_result):
    str = ""
    for keyword in keyword_result:
        str = str + keyword + ","

    strs = str.split(",")
    ss = list(set(strs))
    sss = list(set(strs))
    return ss, sss


def isMaxThen(strs, data, count_nums, max_num):
    datas = data.split(",")
    result = ""
    for d in datas:
        bool = True
        print d
        for i, s in enumerate(strs):
            if s == d:
                print str(i) + " same = " + s + " count_nums = " + str(count_nums[i])
                k = 0
                try:
                    k = int(count_nums[i])
                except Exception, e:
                    print e
                    k = 0
                k += 1
                if k <= max_num:
                    count_nums[i] = k
                    bool = True
                    break
                else:
                    bool = False
                    break
        if bool:
            result = result + d + ","
    return count_nums, result


def groupMemberAction(weeklys):
    weeklyIncludeMemberInfo = namedtuple("weeklyIncludeMemberInfo", ["currWeekly", "startDate", "endDate", "memberOperates"])
    MemberOperate = namedtuple("MemberOperate", ["member_id", "view_project", "view_demand", "favorite_project", "favorite_demand", "publish_project", "publish_demand", "match_project", "match_demand", "push_project", "send_message"])
    weekly4Member = []
    for w in weeklys:
        currWeek = w.currWeekly
        starttime = w.startDate
        endtime = w.endDate
        stime = datetime.datetime.strftime(datetime.datetime.strptime(starttime, "%Y-%m-%d"), "%m-%d")
        etime = datetime.datetime.strftime(datetime.datetime.strptime(endtime, "%Y-%m-%d"), "%m-%d")
        members = Member.objects.filter(add_time__lte=endtime)#.order_by("first_name").exclude(company_id__in=[27, 24765])       #exclude the company is dami capital
        if members:
            memberOperates = []
            for member in members:
                member_id = member.id
                view_project_count = count_view_project(starttime, endtime, member_id)

                #view demand
                view_demand_count = count_view_demand(starttime, endtime, member_id)

                #favorite project
                favorite_project_count = count_favorite_project(starttime, endtime, member_id)

                #favorite demand
                favorite_demand_count = count_favorite_demand(starttime, endtime, member_id)

                match_project_count = count_match_project(starttime, endtime, member_id)

                match_demand_count = count_match_demand(starttime, endtime, member_id)

                push_project_count = count_push_project(starttime, endtime, member_id)

                #publish demand
                send_message_count = count_message(starttime, endtime, member_id)

                #publish project
                publish_project_count = count_publish_project(starttime, endtime, member_id)

                #publish demand
                publish_demand_count = count_publish_demand(starttime, endtime, member_id)

                mo = MemberOperate(member_id, view_project_count, view_demand_count, favorite_project_count, favorite_demand_count, publish_project_count, publish_demand_count, match_project_count, match_demand_count, push_project_count, send_message_count)
                memberOperates.append(mo)

            wim = weeklyIncludeMemberInfo(currWeek, stime, etime, memberOperates)
            weekly4Member.append(wim)
    return weekly4Member


'''
    统计阶段性的用户活跃度，
    根据groups组合计算结果,内容如下：
    0:member_id", "1:view_project", "2:view_demand", "3:favorite_project", "4:favorite_demand", "5:publish_project",
    "6:publish_demand", "7:match_project", "8:match_demand", "9:push_project", "10:send_message"
'''
def countActiveMember(title, datas, groups):
    countResult = namedtuple("countResult", ["currWeekly", "counts"])
    result = []
    result.append(title)
    for d in datas:
        lastCount = 0
        print d.memberOperates
        for m in d.memberOperates:
            count = 0
            for g in groups:
                count += getattr(m, str(g))
            if count > 0:
                lastCount += 1
        cr = countResult(d.currWeekly, lastCount)
        result.append(cr)
    return result

if __name__=="__main__":
    try:
        # aaa = minusMonByMon(starttime)
        # print aaa
        # endtime= '2015-05-31'
        # bool = curr_month_active(starttime, endtime)
        # print bool
        print "---------------start export user detail search----------------------"


        d2 = datetime.date(2015,05,01)
        d1 = datetime.date(2015,05,02)

        weeklys = getWeeklys(d1, d2)
        weekly4Member = groupMemberAction(weeklys)
        print weekly4Member
        # 0:member_id", "1:view_project", "2:view_demand", "3:favorite_project", "4:favorite_demand", "5:publish_project",
        # "6:publish_demand", "7:match_project", "8:match_demand", "9:push_project", "10:send_message"
        result = []
        #周活跃度
        result.append(countActiveMember("周活跃度", weekly4Member, ["view_project", "view_demand", "favorite_project", "favorite_demand", "publish_project", "publish_demand", "push_project", "send_message"]))
        #轻度活跃
        result.append(countActiveMember("轻度活跃", weekly4Member, ["view_project", "view_demand", "favorite_project", "favorite_demand"]))
        #浏览
        result.append(countActiveMember("浏览", weekly4Member, ["view_project", "view_demand"]))
        #收藏
        result.append(countActiveMember("收藏", weekly4Member, ["favorite_project", "favorite_demand"]))
        #重度活跃
        result.append(countActiveMember("重度活跃", weekly4Member, ["publish_project", "publish_demand", "push_project", "send_message"]))
        #发布
        result.append(countActiveMember("发布", weekly4Member, ["publish_project", "publish_demand"]))
        #匹配
        result.append(countActiveMember("匹配", weekly4Member, ["match_project", "match_demand"]))
        #推送
        result.append(countActiveMember("推送", weekly4Member, ["push_project"]))
        #私信
        result.append(countActiveMember("私信", weekly4Member, ["send_message"]))

        print ">>>>>>>>>>>>>.. " + str(result)


        # result.append(countActiveMember("周活跃度", weekly4Member, [1, 2, 3, 4, 5, 6, 9, 10]))
        # #轻度活跃
        # result.append(countActiveMember("轻度活跃", weekly4Member, [1, 2, 3, 4]))
        # #浏览
        # result.append(countActiveMember("浏览", weekly4Member, [1, 2]))
        # #收藏
        # result.append(countActiveMember("收藏", weekly4Member, [3, 4]))
        # #重度活跃
        # result.append(countActiveMember("重度活跃", weekly4Member, [5, 6, 9]))
        # #发布
        # result.append(countActiveMember("发布", weekly4Member, [5, 6]))
        # #匹配
        # result.append(countActiveMember("匹配", weekly4Member, [7, 8]))
        # #推送
        # result.append(countActiveMember("推送", weekly4Member, [9]))
        # #私信
        # result.append(countActiveMember("私信", weekly4Member, [10]))

        # print ">>>>>>>>>>>>>.. " + str(result)

        # findIndustryAndKeyword()

        # starttime = '2015-01-1'
        # endtime= '2015-05-1'
        # data = stay_login_rate(starttime, endtime)
        # data = curr_month_active(starttime, endtime)
        # print str(data)
        # data = every_month_active(starttime, endtime)

        # data = total_active()
        # total_active()
        print "---------------end export user detail search----------------------"

    except Exception,e:
        print e
        logging.error(e)

