#encoding:utf-8
import os,sys
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")

from member.models import Company,CompanyInvestmentField,Member,MemberInvestmentField


company_investment_list=CompanyInvestmentField.objects.all();


for item in company_investment_list:
    company=item.company

    users=Member.objects.filter(company=company)

    for user in users:
        mif=MemberInvestmentField()

        mif.member=user
        mif.tags=item.tags
        mif.revenue = item.revenue
        mif.growth = item.growth
        mif.net_income = item.net_income
        mif.ebita = item.ebita
        mif.deal_type= item.deal_type
        mif.deal_currency=item.deal_currency
        mif.deal_size=item.deal_size
        mif.deal_size_min=item.deal_size_min
        mif.deal_size_max=item.deal_size_max
        mif.country=item.country
        mif.hot=item.hot

        mif.save()

