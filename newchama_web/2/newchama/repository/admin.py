from django.contrib import admin
from repository.models import ListedCompany, AccountingFirm, StockExchange, InvestmentCompany, InvestmentHistory, Keyword
# Register your models here.


class ListedCompanyAdmin(admin.ModelAdmin):
    search_fields = ['name_cn']
    list_display = ('name_cn','name_en','country', 'industry','invest_field','stock_name')
    
class InvestmentCompanyAdmin(admin.ModelAdmin):
    search_fields = ['name_cn']
    list_display = ('name_cn','name_en','country', 'invest_field')


admin.site.register(ListedCompany,ListedCompanyAdmin)
admin.site.register(AccountingFirm)
admin.site.register(StockExchange)
admin.site.register(InvestmentCompany,InvestmentCompanyAdmin)
admin.site.register(InvestmentHistory)
admin.site.register(Keyword)