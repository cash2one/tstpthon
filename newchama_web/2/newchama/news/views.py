from django.shortcuts import render_to_response, redirect, HttpResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
# Create your views here.
from newchama.decorators import login_required


@login_required
def index(request):
    c = {}
    #data = News.objects.all()
    data = []
    c["data"] = data
    return render_to_response("news/list.html", c)


@login_required
@csrf_protect
def add(request):
    c = {}
    c.update(csrf(request))
    msg = ""
    c["msg"] = msg
    return render_to_response("news/add.html", c)


@login_required
@csrf_protect
def edit(request, id):
    c = {}
    c.update(csrf(request))
    msg = ""
    c["msg"] = msg
    return render_to_response("news/edit.html", c)