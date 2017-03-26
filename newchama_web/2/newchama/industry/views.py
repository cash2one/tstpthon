from models import Industry
from django.core import serializers
from django.shortcuts import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def json(request, id):
    try:
        if id != "0":
            industry_list = Industry.objects.filter(father=id)
        else:
            industry_list = Industry.objects.filter(father__isnull=True)
        data = serializers.serialize('json', industry_list)
        return HttpResponse(data, mimetype='javascript/json')
    except ObjectDoesNotExist:
        return HttpResponse({"error", "error"}, mimetype='javascript/json')


def get_industry(request, id):
    try:
        industry = Industry.objects.get(pk=id)
        id = industry.id
        level = industry.level
        father_id = industry.father_id
        father_father_id = industry.father.father_id
        if father_id is None:
            father_id = 0
        if father_father_id is None:
            father_father_id = 0
        data = '{"id":%d,"level":%d ,"father_id":%d ,"father_father_id":%d}' % (id, level, father_id, father_father_id)
        return HttpResponse(data, mimetype='javascript/json')
    except ObjectDoesNotExist:
        return None