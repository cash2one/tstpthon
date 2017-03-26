# -*- coding: utf-8 -*-

TOTAL_SCORE = 100

EXCLUDE_LIST = [u"移动互联网", u"互联网", u"大消费", u"大健康", u"tmt", u"高科技"]

RECOMMEND_WEIGHT = {
    'industry': 0.5,
    'deal_type': 0.2,
    'deal_size': 0.1,
    'currency': 0.05,
    'finance': 0.1,
    'local': 0.05,
    'industry_keyword': 0.6,
    'industry_in_industry': 0.3,
    'industry_invest_industry_one': 0.3,
    'industry_invest_industry_two': 0.3,
    'currency_sure': 1,
    'currency_not_sure': 0.5,
}
