#encoding:utf-8
from django.contrib import admin
from member.models import Member
# Register your models here.


class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'email', 'mobile', 'status', 'role')
    search_fields=('email', 'mobile', 'first_name')
    list_filter = ('status', 'role')
    #date_hierarchy='pro_write_date'#另外一种过滤日期的方式
    #ording=('-pro_write_date',)#可降序排序

admin.site.register(Member, MemberAdmin)
