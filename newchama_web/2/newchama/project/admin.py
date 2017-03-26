from django.contrib import admin
from project.models import Project


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['name_cn']
    list_display = ('name_cn','member','update_time','status')
    
admin.site.register(Project,ProjectAdmin)