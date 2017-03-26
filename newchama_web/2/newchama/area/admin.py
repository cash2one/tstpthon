from django.contrib import admin
from area.models import Continent, Country, Province
# Register your models here.
admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(Province)