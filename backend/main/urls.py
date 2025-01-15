from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.status),
    path('', views.status),
    path('record_incident/', views.record_incident),
    path('rto/auth/register/', views.register_rto),
    path('rto/auth/login/', views.login_rto),
    path('rto/auth/list_all/', views.get_rto_usernames), # For testing
    path('rto/incidents/', views.get_incidents),
]
