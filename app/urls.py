from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('execute-trade/', views.execute_trade, name='execute_trade'),
    path('initiate-payment/', views.initiate_mpesa_payment, name='initiate_payment'),
    path('check-status/<str:checkout_request_id>/', views.check_payment_status, name='check_payment_status'),
    path('mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),
]