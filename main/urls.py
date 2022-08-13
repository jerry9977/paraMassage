from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('api/login/', views.LoginView.as_view(), name="login"),
    path('login/', views.standard_login),
    path('dashboard/', views.dashboard),
    path('customers/', views.customer_list),
    path('checkin/', views.check_in),
    # path('customer_check_in_form/', views.customer_check_in_form),
    path('remedial_check_in_form/', views.remedial_check_in_form),
    path('form_submitted/', views.form_submitted),
    path('upload_receipt/', views.upload_receipt)

] 