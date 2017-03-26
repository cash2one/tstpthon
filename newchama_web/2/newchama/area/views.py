from django.shortcuts import render, HttpResponse
from area.models import Province, City, RegionLevelOne, RegionLevelTwo, RegionLevelThree
from django.core import serializers
from django.shortcuts import get_object_or_404
# Create your views here.


def get_provinces(request, country_id):
    provinces = Province.objects.filter(country_id=country_id).order_by("-sort")
    data = serializers.serialize('json', provinces)
    return HttpResponse(data, mimetype='javascript/json')


def get_cities(request, province_id):
    cities = City.objects.filter(province_id=province_id)
    data = serializers.serialize('json', cities)
    return HttpResponse(data, mimetype='javascript/json')

def get_regionleveltwo(request, regionlevelone_id):
    regionlevelone = get_object_or_404(RegionLevelOne, pk = regionlevelone_id)
    data = serializers.serialize('json', regionlevelone.regionleveltwo_set.all())
    return HttpResponse(data, mimetype='javascript/json')

def get_regionlevelthree(request, regionleveltwo_id):
    regionleveltwo = get_object_or_404(RegionLevelTwo, pk = regionleveltwo_id)
    data = serializers.serialize('json', regionleveltwo.regionlevelthree_set.all())
    return HttpResponse(data, mimetype='javascript/json')
