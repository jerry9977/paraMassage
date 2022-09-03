from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('api/login/', views.LoginView.as_view(), name="login"),
    path('login/', views.standard_login),
    path('dashboard/', views.dashboard),
    path('customers/', views.ClientListView.as_view()),
    path('checkin/', views.check_in),
    path('customers/<int:id>/', views.customer_view),
    path('existing_check_in/<str:token>/', views.existing_remedial_check_in_form),
    # path('customers/list/', views.customer_list),
    # path('customer_check_in_form/', views.customer_check_in_form),
    path('remedial_check_in_form/<str:token>/', views.remedial_check_in_form),
    path('form_submitted/<str:title>', views.form_submitted, name="form_submitted"),
    path('error/<str:title>', views.error_page, name="error_page"),
    path('upload_receipt/', views.upload_receipt)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)