from django.shortcuts import render, render_to_response, redirect, HttpResponse, RequestContext, HttpResponseRedirect


def login_required(func):
    def is_login(request, *args, **nargs):
        if request.session.get('uid', 0) == 0:
            return redirect('adminuser.login')
        return func(request, *args, **nargs)
    return is_login


def permission_required(perm):
    def check_perms(func):
        def is_has_perms(request, *args, **nargs):
            permissions = request.session.get('permissions', '')
            if permissions.find(perm) < 0:
                return redirect('adminuser.nopermission')
            return func(request, *args, **nargs)
        return is_has_perms
    return check_perms

