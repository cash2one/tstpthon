#-*-encoding:utf-8-*-
from django.shortcuts import render, render_to_response, redirect, HttpResponse, RequestContext, get_object_or_404
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib import messages
from backend.decorators import backend_login_required, backend_staff_passes_test, backend_superuser_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

#Dashboard
@backend_login_required
@backend_staff_passes_test
def index(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))

#账户管理
@csrf_protect
def signin(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_url=request.GET['next']
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect("backend.index")
            else:
                messages.warning(request, "您的帐号暂时不可用！")
        else:
            messages.warning(request, "您的帐号或密码输入错误！")

    return render_to_response("backend/signin.html", c, context_instance=RequestContext(request))


def signout(request):
    logout(request)
    return redirect("backend.signin")

@backend_login_required
@backend_staff_passes_test
def profile(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))

@backend_login_required
@backend_staff_passes_test
def change_password(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))


#管理员管理
@backend_login_required
@backend_superuser_passes_test
def admin_list(request):
    c = {}
    c['user_list'] = User.objects.filter(is_staff=True).all()
   
    return render_to_response("backend/admin_list.html", c, context_instance=RequestContext(request))

@backend_login_required
@backend_superuser_passes_test
def admin_add(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))

@backend_login_required
@backend_superuser_passes_test
def admin_detail(request,id):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))

@backend_login_required
@backend_superuser_passes_test
def admin_edit(request,id):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))

@backend_login_required
@backend_superuser_passes_test
def admin_reset_password(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))

@backend_login_required
@backend_superuser_passes_test
def admin_remove(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))


#用户管理
@backend_login_required
@backend_staff_passes_test
def user_list(request):
    return render_to_response("backend/user_list.html", context_instance=RequestContext(request))

@backend_login_required
@backend_staff_passes_test
def user_add(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))

@backend_login_required
@backend_staff_passes_test
def user_detail(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))

@backend_login_required
@backend_staff_passes_test
def user_edit(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))

@backend_login_required
@backend_staff_passes_test
def user_reset_password(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))

@backend_login_required
@backend_staff_passes_test
def user_remove(request):
    return render_to_response("backend/index.html", context_instance=RequestContext(request))


