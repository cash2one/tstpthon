#! /usr/bin/python
# -*- coding:utf-8 -*-

from django.contrib import admin
from monitor.models import InvestEvent, ShanghaiShenzhenNotice, HkNotice, DailyDeal
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin


class InvestEventResource(resources.ModelResource):
    class Meta:
        model = InvestEvent


class ShanghaiShenzhenNoticeAdmin(admin.ModelAdmin):
    list_display = ( 'symbol', 'market_type', 'company', 'title',
                    'notice_type', 'published_date', 'pdf', 'txt')
    search_fields=('symbol','company', 'title', 'body') #搜索条
    #list_filter = (('notice_type_id', DropdownFilter),)
    list_filter = ('market_type', 'notice_type')
    # date_hierarchy='pro_write_date'#另外一种过滤日期的方式
    # ording=('-pro_write_date',)#可降序排序
    #def notice_type_id(self, obj):
    #    return StockMarket.objects.all()
        
    def pdf(self, obj):
        return '<a href="%s"target="_blank">%s</a>' % (obj.pdf_url, obj.pdf_url)
    pdf.allow_tags = True
    pdf.short_description = "PDF URL"

    def txt(self, obj):
        #url = "http://127.0.0.1:8000/monitor/shsz-notice/content/" + str(obj.id)
        url = "http://viper.newchama.com/monitor/shsz-notice/content/" + str(obj.id)
        return '<a href="%s"target="_blank">%s</a>' % (url, url)
    txt.allow_tags = True
    txt.short_description = "TXT URL"


class InvestEventAdmin(ImportExportActionModelAdmin):
    resource_class = InvestEventResource
    list_display = ('investee_abbreviation', 'company_url', 'get_cv1', 'get_cv2', 'get_cv3', 'tag', 'event_scene', 'continent', 'country', 'province', 'city', 'investee_fullname', 'introduction', 'invest_phase', 'amount_formatted', 'scale', 'currency', 'investors', 'financial_advisor', 'time', 'data_source', 'source_itjuzi_url')
    search_fields = ('investee_abbreviation','tag','introduction', 'investors', 'financial_advisor') #搜索条
    list_filter = ('currency', 'event_scene', 'invest_phase', 'scale') #过滤器
    list_per_page = 30

    def amount_formatted(self, obj):
        if obj.amount:
            return format(obj.amount, ",")
        else:
            return obj.amount
    
    amount_formatted.allow_tags = True
    amount_formatted.short_description = "Formated Amount"

    def company_url(self, obj):
        return '<a href="%s"target="_blank">%s</a>' % (obj.website_url, obj.website_url)
    company_url.allow_tags = True
    company_url.short_description = "Firm URL"

    def source_itjuzi_url(self, obj):
        return '<a href="%s"target="_blank">%s</a>' % (obj.source_url, obj.source_url)
    source_itjuzi_url.allow_tags = True
    source_itjuzi_url.short_description = "Source URL"

    def get_cv1(self, obj):
        return ", \n".join([industry_.name_cn for industry_ in obj.cv1.all()])
    get_cv1.short_description = "cv1"

    def get_cv2(self, obj):
        return ", \n".join([industry_.name_cn for industry_ in obj.cv2.all()])
    get_cv2.short_description = "cv2"

    def get_cv3(self, obj):
        return ", \n".join([industry_.name_cn for industry_ in obj.cv3.all()])
    get_cv3.short_description = "cv3"
    # date_hierarchy='pro_write_date'#另外一种过滤日期的方式
    # ording=('-pro_write_date',)#可降序排序


class HkNoticeAdmin(admin.ModelAdmin):
    list_display = ('market_type', 'symbol', 'stock_name',
                    'title', 'get_types', 'time', 'attach_url', 'txt')
    search_fields=('symbol','stock_name', 'title', 'content') #搜索条
    list_filter = ('market_type',)
    def attach_url(self, obj):
        return '<a href="%s"target="_blank">%s</a>' % (obj.url, obj.url)
    attach_url.allow_tags = True
    attach_url.short_description = "Attachment URL"

    def get_types(self, obj):
        return ", ".join([type_.notice_type_name for type_ in obj.types.all()])
    get_types.short_description = "Types"

    def txt(self, obj):
        url = "http://viper.newchama.com/monitor/hknotice/content/" + str(obj.id)
        return '<a href="%s"target="_blank">%s</a>' % (url, url)
    txt.allow_tags = True
    txt.short_description = "TXT URL"


class DailyDealAdmin(admin.ModelAdmin):

    list_display = ('company_short_name', 'stock_symbol', 'cv1',
                    'cv2', 'company_full_name', 'target_company', 'target_company_tags', 'deal_type', 'deal_currency',
                    'deal_amount', 'deal_ratio', 'investor_tags', 'financial_advisor', 'deal_content', 'date',
                    'published_date')
    search_fields=('company_short_name', 'stock_symbol', 'financial_advisor', 'deal_content', 'investor_tags', 'target_company_tags')

# Register your models here.
admin.site.register(InvestEvent, InvestEventAdmin)
admin.site.register(ShanghaiShenzhenNotice, ShanghaiShenzhenNoticeAdmin)
admin.site.register(HkNotice, HkNoticeAdmin)
admin.site.register(DailyDeal, DailyDealAdmin)

