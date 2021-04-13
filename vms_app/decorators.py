from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.shortcuts import redirect

def admin_login_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        role = request.session.get("role")
        print("Role in wrapper_func is: ", role)

        if role != "ADMIN":
            return redirect("admin-login")

        return view_func(request, *args, **kwargs)


    return wrapper_func


def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False