from django.shortcuts import render, render_to_response, redirect, HttpResponse, RequestContext, get_object_or_404
from models import AdminUser, Role
from member_message.models import EditorSay
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import connection
from newchama.decorators import login_required, permission_required
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)

@login_required
def index(request):
    return render_to_response("adminuser/index.html", context_instance=RequestContext(request))


@csrf_protect
def login(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            if username != "" and password != "":
                u = AdminUser.objects.get(username=username)
                if u.check_password(password) and u.isactive:
                    request.session['uid'] = u.id
                    request.session['username'] = username
                    permissions = ""
                    for r in u.role.all():
                        permissions += r.permission+","
                    request.session['permissions'] = permissions
                    return redirect("adminuser.index")
                else:
                    messages.warning(request, "login fail")
            else:
                messages.warning(request, "login fail")
        except ObjectDoesNotExist:
            messages.warning(request, "login fail")
        c['username'] = username
    return render_to_response("adminuser/login.html", c, context_instance=RequestContext(request))


def logout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
    return redirect('adminuser.login')


@login_required
@csrf_protect
def changepassword(request):
    c = {}
    c.update(csrf(request))
    uid = request.session['uid']
    if request.method == 'POST':
        newpassword = request.POST["newpassword"]
        oldpassword = request.POST["oldpassword"]
        try:
            u = AdminUser.objects.get(pk=uid)
            if u.check_password(oldpassword):
                u.make_password(newpassword)
                u.save()
                messages.success(request, "success")
            else:
                messages.warning(request, "old password is not match")
        except ObjectDoesNotExist:
            messages.warning(request, "user is not exist")
    return render_to_response("adminuser/changepassword.html", c, context_instance=RequestContext(request))


@login_required
@csrf_protect
def profile(request):
    c = {}
    c.update(csrf(request))
    uid = request.session['uid']
    try:
        u = AdminUser.objects.get(pk=uid)
        if request.method == 'POST':
            u.email = request.POST["email"]
            u.mobile = request.POST["mobile"]
            u.realname = request.POST["realname"]
            try:
                u.save()
                messages.success(request, "success")
            except Exception, e:
                messages.warning(request, e.message)
    except ObjectDoesNotExist:
        u = AdminUser(username=request.session['username'])
    c['u'] = u
    return render_to_response("adminuser/profile.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("role")
@csrf_protect
def add_role(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        name = request.POST["name"]
        if name == "":
            messages.success(request, "please input role name")
        else:
            try:
                r = Role.objects.get(name=name)
                messages.warning(request, "role name is exist")
            except ObjectDoesNotExist:
                r = Role(name=name)
                r.permission = ",".join(request.POST.getlist("permission"))
                r.save()
                return redirect("role.list")
            c['r'] = r
    return render_to_response("adminuser/add_role.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("role")
@csrf_protect
def edit_role(request, id):
    msg = ""
    c = {}
    c.update(csrf(request))
    r = get_object_or_404(Role, pk=id)
    if request.method == 'POST':
        id_post = request.POST["id"]
        name = request.POST["name"]
        if name == "":
            messages.warning(request, "please input role name")
        else:
            count = Role.objects.filter(name=name).exclude(id=id_post).count()
            if count > 0:
                messages.warning(request, "role name is exist")
            else:
                try:
                    r = Role.objects.get(pk=id_post)
                    r.name = name
                    r.permission = ",".join(request.POST.getlist("permission"))
                    r.save()
                    messages.success(request, "success")
                except Exception, e:
                    messages.warning(request, e.message)
    c['r'] = r
    c['isHasPermission_Role'] = r.is_has_permission("role")
    c['isHasPermission_Adminuser'] = r.is_has_permission("adminuser")
    c['isHasPermission_Company'] = r.is_has_permission("company")
    c['isHasPermission_Member'] = r.is_has_permission("member")
    c['isHasPermission_Project'] = r.is_has_permission("project")
    c['isHasPermission_Demand'] = r.is_has_permission("demand")
    c['isHasPermission_News'] = r.is_has_permission("news")
    c['isHasPermission_Message'] = r.is_has_permission("message")
    c['isHasPermission_Analysis'] = r.is_has_permission("analysis")
    c['isHasPermission_newchamasay'] = r.is_has_permission("newchamasay")
    c['isHasPermission_subscribe'] = r.is_has_permission("subscribe")
    return render_to_response("adminuser/edit_role.html", c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required("role")
def remove_role(request):
    msg = ""
    if request.method == 'POST':
        remove_id = request.POST["id"]
        try:
            r = Role.objects.get(pk=remove_id)
            ul = r.adminuser_set.all()
            if ul:
                msg = "Remove error, There are user in this role!"
            else:
                r.delete()
                msg = "success"
        except ObjectDoesNotExist:
            msg = "Remove error, Please contact the administrator!"

    return HttpResponse(msg)


@login_required
@permission_required("role")
def role_list(request):
    keyword = request.GET.get("keyword", "")
    role_list = Role.objects.filter().order_by("-id")
    if keyword != "":
        role_list = role_list.filter(name__contains=keyword).order_by("-id")
    result_list = role_list
    c = {}
    c["result_list"] = result_list
    c["keyword"] = keyword
    return render_to_response("adminuser/role_list.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("adminuser")
@csrf_protect
def add_adminuser(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        if username == "" or password == "":
            messages.warning(request, "please input you username and password")
        else:
            count = AdminUser.objects.filter(username=username).count()
            if count > 0:
                messages.warning(request, "username is exist")
            else:
                u = AdminUser()
                u.username = username
                u.email = request.POST["email"]
                u.make_password(password)
                u.realname = request.POST["realname"]
                u.mobile = request.POST["mobile"]
                u.isactive = 0
                u.save()
                ur = AdminUser.objects.get(pk=u.id)
                role_ids = request.POST.getlist("roleIds", [])
                if role_ids is not None:
                    for roleid in role_ids:
                        r = Role.objects.get(pk=roleid)
                        ur.role.add(r)
                return redirect("adminuser.list")
    c['roles'] = Role.objects.all()
    return render_to_response("adminuser/add_adminuser.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("adminuser")
@csrf_protect
def edit_adminuser(request, id):
    c = {}
    c.update(csrf(request))
    u = get_object_or_404(AdminUser, pk=id)
    if request.method == 'POST':
        uid_post = request.POST["id"]
        try:
            u = AdminUser.objects.get(pk=uid_post)
            u.email = request.POST["email"]
            u.mobile = request.POST["mobile"]
            u.realname = request.POST["realname"]
            u.isactive = 0
            u.save()

            u.role.clear()
            role_ids = request.POST.getlist("roleIds", [])
            if role_ids is not None:
                for roleid in role_ids:
                    r = Role.objects.get(pk=roleid)
                    u.role.add(r)
            messages.success(request, "success")
        except Exception, e:
            messages.warning(request, e.message)
    c['u'] = u
    c['roles'] = Role.objects.all()
    c['role_selected'] = u.role.all()
    return render_to_response("adminuser/edit_adminuser.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("adminuser")
@csrf_protect
def reset_adminuser_password(request, id):
    msg = ""
    c = {}
    c.update(csrf(request))
    u = get_object_or_404(AdminUser, pk=id)
    if request.method == 'POST':
        password = request.POST["password"]
        if password == "":
            messages.warning(request, "please input password")
        else:
            uid_post = request.POST["id"]
            try:
                u = AdminUser.objects.get(pk=uid_post)
                u.make_password(password)
                u.save()
                messages.success(request, "success")
            except Exception, e:
                messages.warning(request, e.message)
    c['u'] = u
    return render_to_response("adminuser/reset_adminuser_password.html", c, context_instance=RequestContext(request))


@login_required
@permission_required("adminuser")
def adminuser_list(request):
    keyword = request.GET.get("keyword", "")
    adminuser_list = AdminUser.objects.filter(isactive=0).order_by("-id")
    if keyword != "":
        adminuser_list = adminuser_list.filter(username__contains=keyword).order_by("-id")
    result_list = adminuser_list
    c = {}
    c["result_list"] = result_list
    c["keyword"] = keyword
    return render_to_response("adminuser/adminuser_list.html", c, context_instance=RequestContext(request))


@csrf_exempt
@login_required
@permission_required("adminuser")
def remove_adminuser(request):
    msg = ""
    if request.method == 'POST':
        remove_id = request.POST["id"]
        try:
            sql = "update adminuser_adminuser set isactive = 1 where id = " + remove_id
            cursor = connection.cursor()
            cursor.execute(sql)
            msg = "success"
        except ObjectDoesNotExist:
            msg = "Remove error, Please contact the administrator!"

    return HttpResponse(msg)


def nopermission(request):
    return HttpResponse("No Permission")

@login_required
@permission_required("newchamasay")
def newchamasay(request):
    keyword = request.GET.get("keyword", "")
    data = EditorSay.objects.order_by("-id")
    if keyword != "":
        data = data.filter(content_cn__contains=keyword)
    c = {}
    c["result_list"] = data
    c["keyword"] = keyword
    return render_to_response("adminuser/newchamasay_list.html", c, context_instance=RequestContext(request))


@csrf_protect
@login_required
@permission_required("newchamasay")
def add_newchamasay(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        content_cn = request.POST["content_cn"]
        content_en = request.POST["content_en"]
        if content_cn == "" and content_en == "":
            messages.warning(request, "please input content")
        else:
            try:
                m = EditorSay()
                m.content_cn = content_cn
                m.content_en = content_en
                m.save()
                return redirect("newchamasay.list")
            except Exception, e:
                messages.warning(request, e.message)
    return render_to_response("adminuser/add_newchamasay.html", c, context_instance=RequestContext(request))


@csrf_protect
@login_required
@permission_required("newchamasay")
def edit_newchamasay(request, id):
    c = {}
    c.update(csrf(request))
    m = get_object_or_404(EditorSay, pk=id)
    if request.method == 'POST':
        id_post = request.POST["id"]
        content_cn = request.POST["content_cn"]
        content_en = request.POST["content_en"]
        if content_cn == "" and content_en == "":
            messages.warning(request, "please input content")
        else:
            try:
                m = EditorSay.objects.get(pk=id_post)
                m.content_cn = content_cn
                m.content_en = content_en
                m.save()
                return redirect("newchamasay.list")
            except Exception, e:
                messages.warning(request, e.message)
    c['m'] = m
    return render_to_response("adminuser/edit_newchamasay.html", c, context_instance=RequestContext(request))

@csrf_exempt
@login_required
@permission_required("newchamasay")
def remove_newchamasay(request):
    msg = ""
    if request.method == 'POST':
        remove_id = request.POST["id"]
        try:
            m = EditorSay.objects.get(pk=remove_id)
            m.delete()
            msg = "success"
        except Exception, e:
            logger.error(e.message)
            msg = "Remove error, Please contact the administrator!"
    return HttpResponse(msg)