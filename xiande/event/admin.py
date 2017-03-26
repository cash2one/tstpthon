from django.contrib import admin

from event.models import CashEventInfo, EventApply
# Register your models here.
admin.site.register(CashEventInfo)
admin.site.register(EventApply)