from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect

def admin_login_required(view_func):
    print("In admin_login_required decorator")
    def wrapper_func(request, *args, **kwargs):
        role = request.session.get("role")
        print("Role in wrapper_func is: ", req)


        if role != "ADMIN":
            return redirect("admin-login")

        return view_func(request, *args, **kwargs)


    return wrapper_func