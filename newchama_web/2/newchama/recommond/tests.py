# -*- coding:utf-8 -*-
import os,sys
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/adminnewchama/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
from api import GetRecommondScoreItem
from project.models import Project
from member.models import Company


if __name__ == "__main__":
    project = Project.objects.get(pk=587)
    company = Company.objects.get(pk=14898)

    import pudb; pu.db
    recommend_score = GetRecommondScoreItem(project, company)
    print company.name_cn
    print recommend_score.sum_company_score
    print recommend_score.sum_score
    print recommend_score.sum_project_score
