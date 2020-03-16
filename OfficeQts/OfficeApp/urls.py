from django.urls import path
from .views import *

from . import views

urlpatterns = [
    path('', views.Home),
    path('login-dashboard/', views.LoginAdmin),
    path('dashboard/', views.Dashboard),
    path('logout/', views.LogoutAdmin),
]
