"""vms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index),
    path("preregister/", views.preregister),
    path("preregister/check", views.check),
    path("preregister/signup", views.signup),
    path("preregister/verify", views.verify),
    path("stations/register_staff", views.register_new_staff, name="staff_register"),
    path("stations/role_select", views.role_select, name="role_select"),
    path("stations/export_data", views.export_data, name="export_data"),
    path("stations/staff_select", views.staff_select, name="staff-select"),
    path("stations/appointments", views.appointments),
    path("stations/patient_info", views.patient_info),
    path("stations/medical_questions", views.medical_questions),
    path("stations/next_appt", views.next_appt),
    path("stations/vaccine_info", views.vaccine_info),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
