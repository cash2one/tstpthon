#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/adminnewchama/newchama'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
from industry.models import Industry
from project.models import Project, ProjectKeyword, ProjectKeywordAdmin
from member.models import MemberInvestmentField,  Member, MemberFocusKeyword
from recommond.models import MemberRecommendScore
from recommond.models import MatchingWord
from const import FUZZY_WORD_RANK_THRESHOLD
from handler import DealIndustryHandler, DealTypeHandler, DealSizeHandler, DealLocationHandler, DealCurrencyHandler
from util import merge_values, fn_timer
import logging
import logging.handlers
from django.db import transaction


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler('member_recommend.log', maxBytes=10485760, encoding='utf8')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


def load_data():

    member_list = merge_values(list(Member.objects.values('id', 'company_id', 'focus_aspect__name_cn').order_by('id')))
    """ exclude dami capital """
    #members_dict = {d['id']: d for d in filter(lambda x: x['id'] != 27, member_list)}
    members_dict = {d['id']: d for d in member_list}

    """ related member's preference(tag) to member """
    for m in MemberFocusKeyword.objects.all():
        if "tags" not in members_dict[m.member_id]:
            members_dict[m.member_id]["tags"] = []
        members_dict[m.member_id]["tags"].append(m.keyword)

    """ related member's matching table(needs) to member """
    fields = ('id', 'member_id', 'tags', 'deal_currency', 'deal_size_min', 'deal_size_max', 'country_id', 'hot', 'deal_type__id')
    memberinvest_list = merge_values(list(MemberInvestmentField.objects.values(*fields).order_by('id')))
    for need in memberinvest_list:
        member_id = need['member_id']
        if "needs" not in members_dict[member_id]:
            members_dict[member_id]['needs'] = []
        members_dict[member_id]['needs'].append(need)

    """
    for need in MemberInvestmentField.objects.values().order_by('id'):
        member_id = need['member_id']
        if "needs" not in members_dict[member_id]:
            members_dict[member_id]['needs'] = []
        members_dict[member_id]['needs'].append(need)
    """

    """ load industry tbl """
    industry_dict = {d['id']: d for d in Industry.objects.values('id', 'name_cn', 'level', 'father_id').order_by('id')}

    """ load matching word tbl """
    matching_word_lst = MatchingWord.objects.filter(rank__gt=FUZZY_WORD_RANK_THRESHOLD).values_list('word1', 'word2')
    matching_word_dict = {}
    for word1, word2 in matching_word_lst:
        if word1 not in matching_word_dict:
            matching_word_dict[word1] = []
        matching_word_dict[word1].append(word2)

    """ load project keyword tbl """
    project_keyword_dict = {}
    for project_id, keyword in ProjectKeyword.objects.values_list('project_id', 'keyword'):
        if project_id not in project_keyword_dict:
            project_keyword_dict[project_id] = []
        project_keyword_dict[project_id].append(keyword)

    """ load project admin keyword tbl """
    project_keyword_admin_dict = {}
    for project_id, keyword in ProjectKeywordAdmin.objects.values_list('project_id', 'keyword'):
        if project_id not in project_keyword_admin_dict:
            project_keyword_admin_dict[project_id] = []
        project_keyword_admin_dict[project_id].append(keyword)

    return members_dict, industry_dict, matching_word_dict, project_keyword_dict, project_keyword_admin_dict

""" global dict variable """
g_members_dict, g_industry_dict, g_matching_word_dict, g_project_keyword_dict,\
    g_project_keyword_admin_dict = load_data()


def get_single_member_value_dict(member_id):
    if member_id in g_members_dict:
        return g_members_dict[member_id]
    else:
        return None


def load_available_projects():
    return Project.objects.filter(status=2).order_by('-id')#[:10]


def access_fuzzy_word(word_lst):
    fuzzy_word_set = set()
    for word in word_lst:
        if word in g_matching_word_dict:
            if g_matching_word_dict[word]:
                fuzzy_word_set.update(g_matching_word_dict[word])
    fuzzy_word_set.update(word_lst)
    return list(fuzzy_word_set)


def access_project_fuzzy_word(project):
    if project.id in g_project_keyword_dict:
        keywords_lst = g_project_keyword_dict[project.id]
    else:
        keywords_lst = []

    if project.id in g_project_keyword_admin_dict:
        keywords_admin_lst = g_project_keyword_admin_dict[project.id]
    else:
        keywords_admin_lst = []
    return list(set(access_fuzzy_word(keywords_lst) + access_fuzzy_word(keywords_admin_lst)))


def calculate_single_matching_table(buy_need, project, fuzz_word_lst):
    score_item = MemberRecommendScore()
    score_item.project_id = project.id
    score_item.member_id = buy_need['member_id']
    industry_handler = DealIndustryHandler(fuzz_word_lst)
    score_item.need_type = 1
    score_item.need_id = buy_need['id']

    deal_type_handler = DealTypeHandler()
    deal_size_handler = DealSizeHandler()
    deal_currency_handler = DealCurrencyHandler()
    deal_location_handler = DealLocationHandler()
    chain = deal_location_handler + deal_currency_handler + deal_size_handler +\
        deal_type_handler + industry_handler
    chain.use_hook(project=project, need=buy_need, score_item=score_item)
    if score_item.sum_member_score > 0:
        logger.info("buy_need:{0:.0f} score:{1:.0f}".format(buy_need['id'], score_item.sum_member_score))
        return score_item
    else:
        return None


def calculate_matching_tables_score(project, member_dict, fuzzy_word_lst):
    score_lst = []
    if 'needs' in member_dict:
        for tbl in member_dict['needs']:
            res = calculate_single_matching_table(tbl, project, fuzzy_word_lst)
            if res:
                score_lst.append(res)
    if len(score_lst) > 0:
        score_lst.sort(key=lambda x: x.sum_member_score, reverse=True)
        return score_lst[0]
    else:
        return None


@fn_timer
@transaction.atomic
def commit_project_recommends(score_item_lst):
    for score_item in score_item_lst:
        score_item.save()
        logger.info("score_item:{0:.0f} save successfully".format(score_item.sum_member_score))


def compute_score(project):
    score_item_lst = []
    fuzzy_word_lst = access_project_fuzzy_word(project)

    MemberRecommendScore.objects.exclude(is_in_control_panel=True).filter(is_man=False, project=project).delete()
    ##test
    #res = calculate_matching_tables_score(project, g_members_dict[153], fuzzy_word_lst)
    #score_item_lst.append(res)

    for member_dict in g_members_dict.values():
        res = calculate_matching_tables_score(project, member_dict, fuzzy_word_lst)
        if res:
            score_item_lst.append(res)
    return score_item_lst


def entry():
    project_list=Project.objects.filter(status=2).order_by('-id')[:10]

    ##test
    #project_list = Project.objects.filter(pk=422)

    total_score_item_lst = []
    for project in project_list:
        total_score_item_lst.extend(compute_score(project))

    commit_project_recommends(total_score_item_lst)

if __name__ == '__main__':
    #import pudb; pu.db
    entry()
