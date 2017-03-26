import os,sys
sys.path.append(os.path.abspath('../..'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")

from services.models import ProjectCustomerTargetCompany,ListedCompany,InvestmentCompany,Company,Project
from sales.views import recommendCampany

_project_list=Project.objects.exclude(status=5).order_by('-id').all()
for _project in _project_list:

    _list =recommendCampany(False, _project,1000)

    print _list
    ProjectCustomerTargetCompany.objects.filter(project=_project,is_man=False).delete()

    for item in _list:
        
        
        _t=ProjectCustomerTargetCompany.objects.filter(project=_project,company_id=item['id'],company_type=item['type'])
        
        if len(_t) ==0:
            _target_company =ProjectCustomerTargetCompany()
            _target_company.project=_project
            _target_company.company_id=item['id']
            _target_company.company_name_cn=item['name_cn']
            _target_company.company_name_en=item['name_en']
            _target_company.company_short_name_cn=item['short_name_cn']
            _target_company.company_short_name_en=item['short_name_en']
            _target_company.company_logo=item['logo']
            _target_company.has_user=item['has_user']
            _target_company.company_field=item['company_field']
            _target_company.company_type=item['type']
            _target_company.target_reason=item['recommendReason']

            _target_company.save()
