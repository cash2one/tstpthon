#! /usr/bin/python
# -*- coding:utf-8 -*-
import itertools
import time
from functools import wraps
import os
import sys
import urllib2
import json
import csv
import datetime
from repository.models import Tag
from member.models import MemberInvestmentField,  Member, MemberFocusKeyword
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/adminnewchama/newchama'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")


def merge_values(values):
    """
    When you call values() on a queryset where the Model has a ManyToManyField
    and there are multiple related items, it returns a separate dictionary for each
    related item. This function merges the dictionaries so that there is only
    one dictionary per id at the end, with lists of related items for each.
    """
    grouped_results = itertools.groupby(values, key=lambda value: value['id'])

    merged_values = []
    for k, g in grouped_results:
        groups = list(g)
        merged_value = {}
        for group in groups:
            for key, val in group.iteritems():
                if not merged_value.get(key):
                    merged_value[key] = val
                elif val != merged_value[key]:
                    if isinstance(merged_value[key], list):
                        if val not in merged_value[key]:
                            merged_value[key].append(val)
                    else:
                        old_val = merged_value[key]
                        merged_value[key] = [old_val, val]
        merged_values.append(merged_value)
    return merged_values


def get_exchange_rate(currency_from, currency_to):
    yql_base_url = "https://query.yahooapis.com/v1/public/yql"
    yql_query = 'select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20("'+currency_from+currency_to+'")'
    paras = "&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
    yql_query_url = yql_base_url + "?q=" + yql_query + paras
    try:
        yql_response = urllib2.urlopen(yql_query_url)
        try:
            yql_json = json.loads(yql_response.read())
            rate = float(yql_json['query']['results']['rate']['Rate'])
            return rate
        except (ValueError, KeyError, TypeError):
            return None
    except IOError, e:
        return None


def update_exchange_rate():
    rates = []
    fields = ['source_currency', 'target_currency', 'rate', 'date']
    with open('exchange_rate.csv', 'rU') as fr:
        rows = csv.DictReader(fr, fieldnames=fields, delimiter=',')
        for row in rows:
            rates.append(row)

    for rate_info in rates:
        latest_rate = get_exchange_rate(rate_info['source_currency'],
                                        rate_info['target_currency'])
        if latest_rate:
            rate_info['rate'] = latest_rate
            rate_info['date'] = datetime.datetime.today()

    with open('exchange_rate.csv', 'wb') as fw:
        dw = csv.DictWriter(fw, fieldnames=fields)
        for rate_info in rates:
            dw.writerow(rate_info)

def convert_to_cny(source_currency, amount):
    if source_currency == "CNY":
        return amount
    if not amount:
        return amount
    fields = ['source_currency', 'target_currency', 'rate', 'date']

    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, 'exchange_rate.csv')
    with open(file_path, 'rU') as fr:
        rows = csv.DictReader(fr, fieldnames=fields, delimiter=',')
        for row in rows:
            if row['source_currency'] == source_currency:
                return amount*float(row['rate'])

""" load tag library """
def find_parent(tag, dic, weight):
    """ Recursion Base """
    if dic[tag] is None:
        return [(tag, weight)]
    """ Recursion Step """
    parents = [(tag, weight)]
    for x in dic[tag]:
        parents += find_parent(x, dic, weight-20)
    return parents


def load_tag_library():
    raw = {d['name']: d['sub_name'].split(",") for d in Tag.objects.values('name', 'sub_name')}
    dic = {} # temp dict  child <---> parents weight(80)
    for k, v in raw.iteritems():
        if k not in dic:
            dic[k] = None
        if len(v) > 0:
            for x in v:
                if x not in dic:
                    dic[x] = [k]
                else:
                    if x != k:
                        if dic[x] is None:
                            dic[x] = []
                        dic[x].append(k)
                    else:
                        # Case: B2B : B2B
                        pass
    res = {}
    for k in dic.keys():
        #res[k] = list(set(find_parent(k, dic)))
        res[k] = find_parent(k, dic, 100)
    return res


g_tag_library = load_tag_library()


def reload_tag():
    global g_tag_library
    g_tag_library = load_tag_library()
    

def access_tag_fuzzy_word(word_lst):
    fuzzy_word_set = set()
    for word in word_lst:
        if word in g_tag_library:
            if g_tag_library[word]:
                fuzzy_word_set.update(g_tag_library[word])
    return list(fuzzy_word_set)


def get_single_need_data(need_id):
    fields = ('id', 'member_id', 'tags', 'deal_currency','deal_size_min', 'deal_size_max', 'country_id','hot', 'deal_type__id', 'multi_currency')
    try:
        data = merge_values(list(MemberInvestmentField.objects.filter(id=need_id).values(*fields)))
        if len(data) > 0:
            data = data[0]
        else:
            data = None
    except MemberInvestmentField.DoesNotExist:
        data = None
    return data

def load_members_data():
    member_list = merge_values(list(Member.objects.values('id', 'company_id', 'focus_aspect__name_cn').order_by('id')))
    """ exclude dami capital """
    members_dict = {d['id']: d for d in filter(lambda x: x['company_id'] != 27, member_list)}
    #members_dict = {d['id']: d for d in member_list}

    """ related member's preference(tag) to member """
    for m in MemberFocusKeyword.objects.exclude(member__company_id=27):
        if "tags" not in members_dict[m.member_id]:
            members_dict[m.member_id]["tags"] = []
        members_dict[m.member_id]["tags"].append(m.keyword)

    """ related member's matching table(needs) to member """
    fields = ('id', 'member_id', 'tags', 'deal_currency',
              'deal_size_min', 'deal_size_max', 'regionlevelone__id',
              'regionleveltwo__id', 'regionlevelthree__id', 'hot',
              'deal_type__id', 'multi_currency')

    needs_query = MemberInvestmentField.objects.exclude(member__company_id=27).values(*fields).order_by('id')
    memberinvest_list = merge_values(list(needs_query))
    for need in memberinvest_list:
        member_id = need['member_id']
        if "needs" not in members_dict[member_id]:
            members_dict[member_id]['needs'] = []
        members_dict[member_id]['needs'].append(need)
    return members_dict


def get_single_member_value_dict(member_id):
    all_members_dict = load_members_data()
    if member_id in all_members_dict:
        return all_members_dict[member_id]
    else:
        return None


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s: %s seconds" %
               (function.func_name, str(t1-t0))
               )
        return result
    return function_timer



