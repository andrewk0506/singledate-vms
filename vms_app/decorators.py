from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.shortcuts import redirect

def admin_role_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        role = request.session.get("role")
        if role != "ADMIN":
            logout(request.user)
            print("role is currently:!!!!!!!!!! ", role)
            context = {"message": "You need to login to access this page"}
            return redirect("account_login")

        return view_func(request, *args, **kwargs)


    return wrapper_func
