from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from backend.settings import BACKEND_LOGIN_URL

def backend_staff_check(user):
    return user.is_staff

def backend_superuser_check(user):
    return user.is_superuser

def backend_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=BACKEND_LOGIN_URL):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def backend_staff_passes_test(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=BACKEND_LOGIN_URL):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        backend_staff_check,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def backend_superuser_passes_test(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=BACKEND_LOGIN_URL):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        backend_superuser_check,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator