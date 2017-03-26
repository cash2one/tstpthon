#coding=utf-8
from django import template
from django.utils.translation import ugettext_lazy as _
import re
import datetime
from django.utils.timezone import is_aware, utc
from django.utils.html import avoid_wrapping
register = template.Library()

@register.filter(name="formatCurrency")
def formatCurrency(value):
    if value is None or value == "" or value == "0" or value == 0:
        return "未公布"
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
    if result != "未公布":
        return currency_type + " " + formatCurrency(value)
    else:
        return result

@register.filter(name="formatCurrency4Preference")
def formatCurrency4Preference(value):
    if value is None or value == "" or value == "None" or value == 0:
        return ""
    elif value == "0" or value == 0:
        return "0"
    else:
        return formatCurrency(value)


@register.filter(name="formatPercent")
def formatPercent(value):
    if value is None or value == "" or value == "None" or value == 0:
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
        return "未公布"
    else:
        return str(int(value)) + " %"


@register.filter(name="replaceLine")
def replaceLine(value):
    return value.replace("<br/>", "\n");


@register.filter(name="replaceBrToEmpty")
def replaceBrToEmpty(value):
    return value.replace("<br/>", " ");

@register.filter(name="recommendType")
def recommendType(value):
    if value is None or value == "" or value == "0" or value == 0:
    	return ""
    else:
    	return _(value)

@register.filter(name="checkNone")
def checkNone(value):
    if value is None or value is False or value == "None" or value == 0:
        return "未公布"
    else:
    	return value

@register.filter(name="handleFileSize")
def handleFileSize(value):
    value = value / 1024 / 1024;
    return "%.4s" % (str(value)) + " MB"


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
    location = "未公布"
    if city:
        location = country.name_cn + " " + city.name_cn
    elif country:
        location = country.name_cn
    return location


@register.filter(name="formatDate")
def formatDate(value):
    return datetime.datetime.strftime(datetime.datetime.strptime(value, "%Y-%m-%d"), "%m-%d")