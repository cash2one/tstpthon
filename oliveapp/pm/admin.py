from django.contrib import admin

from pm.models import Customer,Project,Task

# Register your models here.

def make_start(modeladmin, request, queryset):
    queryset.update(task_status=Task.TASK_STATUS[1][0])
make_start.short_description = Task.TASK_STATUS[1][1]

def make_test(modeladmin, request, queryset):
    queryset.update(task_status=Task.TASK_STATUS[2][0])
make_test.short_description = Task.TASK_STATUS[2][1]

def make_finish(modeladmin, request, queryset):
    queryset.update(task_status=Task.TASK_STATUS[3][0])
make_finish.short_description = Task.TASK_STATUS[3][1]

def make_money_start(modeladmin, request, queryset):
    queryset.update(task_money_status=Task.TASK_MONEY_STATUS[1][0])
make_money_start.short_description = Task.TASK_MONEY_STATUS[1][1]

def make_money_finish(modeladmin, request, queryset):
    queryset.update(task_money_status=Task.TASK_MONEY_STATUS[2][0])
make_money_finish.short_description = Task.TASK_MONEY_STATUS[2][1]

class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['name']

class ProjectAdmin(admin.ModelAdmin):
    list_filter = ('customer__name',)
    search_fields = ['name']
    list_display = ('name', 'customer')

class TaskAdmin(admin.ModelAdmin):
    exclude = ('add_time','operator')
    list_filter = ('task_type', 'task_status','task_money_status','project__name')
    search_fields = ['name']
    actions = [make_start,make_test,make_finish,make_money_start,make_money_finish]
    list_display = ('project','name', 'task_type','start_time','end_time','money' ,'colored_status','colored_money_status')
    def save_model(self, request, obj, form, change):
        obj.operator = request.user
        obj.save()


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)