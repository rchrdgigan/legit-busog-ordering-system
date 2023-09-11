from django.shortcuts import redirect
from django.http import HttpResponse

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(response, *args, **kwargs):
            group = None
            if response.user.groups.exists():
                group = response.user.groups.all()[0].name

                if group in allowed_roles:
                    return view_func(response, *args, **kwargs)
                else:
                    return HttpResponse('You are not authorize to view this page')
        return wrapper_func
    return decorator