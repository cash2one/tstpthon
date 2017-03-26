#coding=utf-8
from django import template
import re
from services.helper import Helper
from services.models import ProjectKeyword
from django.utils.translation import ugettext_lazy as _
import datetime
from django.utils.timezone import is_aware, utc
from django.utils.html import avoid_wrapping
register = template.Library()

@register.filter(name="formatCurrency")
def formatCurrency(value):
    if value is None or value == "" or value == "0" or value == 0:
        return "N/A"
    s = str(value).split(".")[0][::-1]
    i = 0
    sep = ","
    groups = []
    while i < len(s):
        groups.append(s[i: i + 3])
        i += 3
    retval = sep.join(groups)[::-1]
    if value < 0:
        return '-%s' % retval
    return retval

@register.filter(name="formatCurrency2")
def formatCurrency2(value, currency_type):
    result = formatCurrency(value)
    if result != "N/A":
        if currency_type == "USD":
            currency_type = "$"
        elif currency_type == "EUR":
            currency_type = "€"
        else:
            currency_type = "¥"
        return currency_type + " " + formatCurrency(value)
    else:
        return result

@register.filter(name="formatCurrency4Preference")
def formatCurrency4Preference(value):
    if value is None or value == "" or value == "None":
        return ""
    elif value == "0" or value == 0:
        return "0"
    else:
        return formatCurrency(value)


@register.filter(name="formatPercent")
def formatPercent(value):
    if value is None or value == "" or value == "None":
        return ""
    else:
        return int(value)


@register.filter(name="showPercent")
def showPercent(value):
    if value is None or value == "" or value == "0" or value == 0:
        return "-"
    else:
        return int(value)


@register.filter(name="showPercent2")
def showPercent2(value):
    if value is None or value == "" or value == "0" or value == 0:
        return "N/A"
    else:
        return str(int(value)) + " %"


@register.filter(name="replaceLine")
def replaceLine(value):
    return value.replace("<br/>", "\n");


@register.filter(name="replaceBrToEmpty")
def replaceBrToEmpty(value):
    return value.replace("<br/>", " ");

@register.filter(name="urlEncode")
def urlEncode(value):
    return Helper.url_encode(value)

@register.filter(name="recommendType")
def recommendType(value):
    if value is None or value == "" or value == "0" or value == 0:
    	return ""
    else:
    	return _(value)

@register.filter(name="checkNone")
def checkNone(value):
    if value is None or value is False or value == "None" :
    	return "N/A"
    else:
    	return value


@register.filter(name="getKeywordByProject")
def getKeywordByProject(project):
    keywords_list=[]
    for kv in ProjectKeyword.objects.filter(project=project):
        keywords_list.append(kv.keyword)
    return ','.join(keywords_list)


@register.filter(name="custom_time_line")
def custom_time_line(d, now=None):
    chunks = (
        (60 * 60 * 24 * 7, "%d周之前"),
        (60 * 60 * 24, "%d日之前"),
        (60 * 60, "%d小时之前"),
        (60, '%d分钟之前')
    )
    # Convert datetime.date to datetime.datetime for comparison.
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)

    if not now:
        now = datetime.datetime.now(utc if is_aware(d) else None)

    delta = (now - d)
    # ignore microseconds
    since = delta.days * 24 * 60 * 60 + delta.seconds
    result = ""
    for i, (seconds, name) in enumerate(chunks):
        if since > seconds:
            count = 1
            if i == 1:
                count = 2
            elif i > 1:
                count = since // seconds
            result = name % count
            break
    return result


cal = {'0':'日','1':'一','2':'二','3':'三','4':'四','5':'五','6':'六'}

@register.filter(name="caculate")
def caculate(time):
    now = datetime.datetime.now()
    time = time + datetime.timedelta(hours=8)               #handle time show with message
    if time.day == now.day:
        result = time.strftime('%H:%M:%S')
    elif time.isocalendar()[1] == now.isocalendar()[1]:
        week_num = time.strftime('%w')
        week_character = cal[week_num]
        result = "星期"+week_character
    else:
        result = str(time.year)+"年"+str(time.month)+"月"+str(time.day)+"日"
    return result


@register.filter(name="cut_str")
def cut_str(str, length=10):
    if str is None or len(str) == 0:
        return ""
    """
    截取字符串，使得字符串长度等于length，并在字符串后加上省略号
    """
    is_encode = False
    try:
        str_encode = str.encode('gb18030') #为了中文和英文的长度一致（中文按长度2计算）
        is_encode = True
    except:
        pass
    if is_encode:
        l = length*2
        if l < len(str_encode):
            l = l - 3
            str_encode = str_encode[:l]
            try:
                str = str_encode.decode('gb18030') + '...'
            except:
                str_encode = str_encode[:-1]
                try:
                    str = str_encode.decode('gb18030') + '...'
                except:
                    is_encode = False
    if not is_encode:
        if length < len(str):
            length = length - 2
            return str[:length] + '...'
    return str


@register.filter(name="merge_location")
def merge_location(country, city):
    location = "N/A"
    if city:
        location = city.name_cn #country.name_cn + " " + city.name_cn
    elif country:
        location = country.name_cn
    return location
