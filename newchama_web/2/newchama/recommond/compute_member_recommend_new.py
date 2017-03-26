import os
import sys
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/adminnewchama/newchama'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
from project.models import Project, ProjectKeyword, ProjectKeywordAdmin
from recommond.models import MemberRecommendScore, ProjectTargetMemberDetail
from const import EXCLUDE_LIST
from handler import DealIndustryHandler, DealTypeHandler, DealSizeHandler, DealLocationHandler, DealCurrencyHandler
from util import merge_values, fn_timer, access_tag_fuzzy_word, load_members_data, get_single_need_data
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
logging.disable(logging.DEBUG)


def access_project_tag_fuzzy_word(project):
    keywords_lst = ProjectKeyword.objects.filter(project_id=project.id).values_list('keyword', flat=True)
    keywords_lst = [word for word in keywords_lst if word not in EXCLUDE_LIST]
    keywords_admin_lst = ProjectKeywordAdmin.objects.filter(project_id=project.id).values_list('keyword', flat=True)
    keywords_admin_lst = [word for word in keywords_admin_lst if word not in EXCLUDE_LIST]
    return list(set(access_tag_fuzzy_word(keywords_lst) + access_tag_fuzzy_word(keywords_admin_lst)))


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
    chain = deal_location_handler + deal_size_handler + deal_currency_handler +\
        deal_type_handler + industry_handler
    chain.use_hook(project=project, need=buy_need, score_item=score_item)
    if score_item.sum_member_score > 0:
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


@transaction.atomic
def commit_project_recommends(score_item_lst):
    for score_item in score_item_lst:
        score_item.save()


def compute_score(project):
    score_item_lst = []
    g_members_dict = load_members_data()
    MemberRecommendScore.objects.exclude(is_in_control_panel=True).filter(is_man=False, project=project).delete()
    fuzzy_word_lst = access_project_tag_fuzzy_word(project)
    fuzzy_word_lst = [(tag, weight) for tag, weight in fuzzy_word_lst if tag not in EXCLUDE_LIST]
    ##test
    #res = calculate_matching_tables_score(project, g_members_dict[153], fuzzy_word_lst)
    #score_item_lst.append(res)

    existed_members = ProjectTargetMemberDetail.objects.filter(project=project).values_list('member_id',
                                                                                            flat=True)
    potential_members = {k: g_members_dict[k] for k in g_members_dict.keys() if k not in existed_members}
    for member_dict in potential_members.values():
        res = calculate_matching_tables_score(project, member_dict, fuzzy_word_lst)
        if res:
            score_item_lst.append(res)
    commit_project_recommends(score_item_lst)
    return score_item_lst


def compute_recommend_projects(need_id):
    score_item_lst = []
    MemberRecommendScore.objects.exclude(is_in_control_panel=True).filter(is_man=False, need_id=need_id).delete()

    # filter exist  projects
    existed_projects = MemberRecommendScore.objects.filter(need_id=need_id, is_in_control_panel=True)\
        .values_list('project__id', flat=True)
    project_list = Project.objects.filter(status=2).exclude(id__in=existed_projects)
    for project in project_list:
        fuzzy_word_lst = access_project_tag_fuzzy_word(project)
        fuzzy_word_lst = [(tag, weight) for tag, weight in fuzzy_word_lst if tag not in EXCLUDE_LIST]
        need = get_single_need_data(need_id)
        if need:
            res = calculate_single_matching_table(need, project, fuzzy_word_lst)
            if res and res.sum_member_score > 0:
                score_item_lst.append(res)
    commit_project_recommends(score_item_lst)


def entry():
    
    #project_list=Project.objects.filter(status=2).order_by('-id')[:10]

    #test
    project_list = Project.objects.filter(pk=422)

    total_score_item_lst = []
    for project in project_list:
        total_score_item_lst.extend(compute_score(project))

    #commit_project_recommends(total_score_item_lst)

if __name__ == '__main__':
    #import pudb; pu.db
    entry()
