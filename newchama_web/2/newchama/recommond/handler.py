#! /usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import division
from const import TOTAL_SCORE, RECOMMEND_WEIGHT
from util import access_tag_fuzzy_word, convert_to_cny
from const import EXCLUDE_LIST

class Handler (object):
    """The base class for all the handlers"""

    def __init__(self):
        self.next_handler = None

    def __add__(self, new_handler):
        """Used to append handlers to each other"""
        if not isinstance(new_handler, Handler):
            raise TypeError('Handler.__add__() expects Handler')
        if self.next_handler:
            self.next_handler + new_handler
        else:
            self.next_handler = new_handler
        return self

    def use_hook(self, **kwargs):
        """Wrapper around the hook method"""
        if self.next_handler:
            if not self.next_handler.use_hook(**kwargs):
                return False
        return self.hook(**kwargs)

    def hook(self, **kwargs):
        """Default hook method to be overridden in subclasses"""
        return True


class DealIndustryHandler(Handler):
    def __init__(self, fuzzy_words_lst):
        super(DealIndustryHandler, self).__init__()
        self.fuzz_words_lst = fuzzy_words_lst

    def hook(self, **kwargs):
        matched_word_lst = []
        score_item = kwargs['score_item']
        is_industry_match = False

        if kwargs['need']:
            need_tags = kwargs['need']['tags'].split(',')
        else:
            need_tags = []
        fuzz_need_tags = access_tag_fuzzy_word(need_tags)
        fuzz_need_tags = [(tag, weight) for tag, weight in fuzz_need_tags if tag not in EXCLUDE_LIST]
        mapping_tags_dic = {}
        for tag, weight in fuzz_need_tags:
            mapping_tags_dic[tag] = weight

        for word, weight in self.fuzz_words_lst:
            if word in mapping_tags_dic:
                matched_word_lst.append((word, weight))


        if len(matched_word_lst) > 0:
            is_industry_match = True
            max_weight = max([weight for _, weight in matched_word_lst]) / 100
            score_item.member_score_industry_keyword = TOTAL_SCORE * RECOMMEND_WEIGHT['industry'] *\
                RECOMMEND_WEIGHT['industry_keyword'] * max_weight
            score_item.matched_tags = ",".join([word + u"(" + unicode(weight) + u")" for word, weight in matched_word_lst])
        return is_industry_match


class DealTypeHandler(Handler):

    def hook(self, **kwargs):
        is_deal_type_matched = False
        buy_need = kwargs['need']
        project = kwargs['project']
        score_item = kwargs['score_item']
        deal_type_lst = []
        if isinstance(buy_need['deal_type__id'], list):
            deal_type_lst.extend(buy_need['deal_type__id'])
        elif isinstance(buy_need['deal_type__id'], int):
            deal_type_lst.append(buy_need['deal_type__id'])
        elif buy_need['deal_type__id'] is None:
            return is_deal_type_matched
        else:
            raise Exception

        project_deal_type_lst = [t.id for t in project.deal_type.all()]
        for deal_type in project_deal_type_lst:
            if deal_type in deal_type_lst:
                is_deal_type_matched = True
                break

        if is_deal_type_matched:
            score_item.member_score_deal_type = TOTAL_SCORE * RECOMMEND_WEIGHT['deal_type']

        return is_deal_type_matched

class DealCurrencyHandler(Handler):
    def hook(self, **kwargs):
        is_deal_currency_matched = False
        is_deal_currency_partly_matched = False
        buy_need = kwargs['need']
        project = kwargs['project']
        buy_need_currency = buy_need['multi_currency']
        if buy_need_currency:
            buy_need_currency = [int(cur) for cur in buy_need_currency.split(',')]
        score_item = kwargs['score_item']
        if project.multi_currency is None:      #Terry modify if multi_currency is empty 20151009
            pass
        else:
            project_currencies = [int(cur) for cur in project.multi_currency.split(',')]
            if len(set(project_currencies) & set(buy_need_currency)) > 0:
                is_deal_currency_matched = True
            elif 99 in buy_need_currency:
                is_deal_currency_partly_matched = True
            elif 0 in buy_need_currency:
                pass

        if is_deal_currency_matched:
            score_item.member_score_currency = TOTAL_SCORE * RECOMMEND_WEIGHT['currency'] * \
                                               RECOMMEND_WEIGHT['currency_sure']
        elif is_deal_currency_partly_matched:
            score_item.member_score_currency = TOTAL_SCORE * RECOMMEND_WEIGHT['currency'] * \
                                               RECOMMEND_WEIGHT['currency_not_sure']
        return is_deal_currency_matched or is_deal_currency_partly_matched


class DealSizeHandler(Handler):
    def hook(self, **kwargs):
        is_deal_size_matched = False
        buy_need = kwargs['need']
        project = kwargs['project']
        score_item = kwargs['score_item']
        currency_dict = {1: 'CNY', 2: 'USD', 3: 'EUR'}
        project_source_currency = currency_dict.get(project.pay_currency, None)
        need_source_currency = currency_dict.get(buy_need['deal_currency'], None)

        if project.deal_size and project_source_currency and need_source_currency:
            project_converted_size = convert_to_cny(project_source_currency, project.deal_size)
            need_size_min = convert_to_cny(need_source_currency, float(buy_need['deal_size_min']))
            need_size_max = convert_to_cny(need_source_currency, float(buy_need['deal_size_max']))
            scale_size_min = need_size_min / 1.2
            scale_size_max = need_size_max * 1.2

            if scale_size_min <= project_converted_size <= scale_size_max:
                is_deal_size_matched = True
                score_item.member_score_deal_size = TOTAL_SCORE * RECOMMEND_WEIGHT['deal_size']
        else:
            is_deal_size_matched = True
            score_item.member_score_deal_size = TOTAL_SCORE * RECOMMEND_WEIGHT['deal_size']
        return is_deal_size_matched


class DealLocationHandler(Handler):
    def hook(self, **kwargs):
        is_deal_location_matched = False
        buy_need = kwargs['need']
        project = kwargs['project']
        score_item = kwargs['score_item']
        need_regionlevelone = buy_need.get('regionlevelone__id', None)
        if project.regionlevelone and need_regionlevelone:
            if project.regionlevelone.id == need_regionlevelone:
                is_deal_location_matched = True
                if project.regionleveltwo:
                    if project.regionleveltwo.id == buy_need.get('regionleveltwo__id', 0):
                        score_item.member_score_local = TOTAL_SCORE * RECOMMEND_WEIGHT['local']
                else:
                    score_item.member_score_local = TOTAL_SCORE * RECOMMEND_WEIGHT['local'] * \
                                                    RECOMMEND_WEIGHT['local-partly']
        else:
            is_deal_location_matched = True  # location data in project or needs is not complete

        if is_deal_location_matched:
            score_item.sum_member_score = sum([score_item.member_score_industry_keyword,
                                               score_item.member_score_deal_type,
                                               score_item.member_score_deal_size,
                                               score_item.member_score_currency,
                                               score_item.member_score_local])
        return is_deal_location_matched
