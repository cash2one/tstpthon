#encoding:utf-8
import os,sys

sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('/var/www/newchama'))
import newchama.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newchama.settings")
from project.models import Project
from recommond.models import RecommondItem


import csv

writer1 = csv.writer(file('tb1.csv', 'w'))
writer2 = csv.writer(file('tb2.csv', 'w'))

reload(sys)
sys.setdefaultencoding( "utf-8")

num=10000

p_list=Project.objects.order_by('-id')[0:num]
 
writer1.writerow(["项目ID", "项目名称", "投资方向匹配","战略投资人","有相同投资行业","有相似投资行业"])
for project in p_list:
    num1=RecommondItem.objects.filter(project=project,target_reason='investment orientation').count()
    num2=RecommondItem.objects.filter(project=project,target_reason='public company within the same industry').count()
    num3=RecommondItem.objects.filter(project=project,target_reason='investor within the same industry').count()
    num4=RecommondItem.objects.filter(project=project,target_reason='invested in similar companies').count() 
    
    writer1.writerow([unicode(project.id), unicode(project.name_cn[:20]),unicode(num1),unicode(num2),unicode(num3),unicode(num4)])

 
writer2.writerow(["项目ID", "项目名称", "小于20","20-30","30-40","40-50","50-60",'60-70','70-80','大于80']) 

for project in p_list:     
    num1=RecommondItem.objects.filter(project=project,sum_score__lte=20).count()
    num2=RecommondItem.objects.filter(project=project,sum_score__gt=20,sum_score__lte=30).count()
    num3=RecommondItem.objects.filter(project=project,sum_score__gt=30,sum_score__lte=40).count()
    num4=RecommondItem.objects.filter(project=project,sum_score__gt=40,sum_score__lte=50).count()
    num5=RecommondItem.objects.filter(project=project,sum_score__gt=50,sum_score__lte=60).count() 
    num6=RecommondItem.objects.filter(project=project,sum_score__gt=60,sum_score__lte=70).count() 
    num7=RecommondItem.objects.filter(project=project,sum_score__gt=70,sum_score__lte=80).count() 
    num8=RecommondItem.objects.filter(project=project,sum_score__gt=80).count()
    
    writer2.writerow([str(project.id), project.name_cn[:20],str(num1),str(num2),str(num3),str(num4),str(num5),str(num6),str(num7),str(num8)]) 



