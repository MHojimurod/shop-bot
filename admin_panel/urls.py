from os import name
from django.urls import path
from .views import *


urlpatterns = [
    path('',home, name="home"),
    path('login/', dashboard_login, name="login"),
    path('logout/', dashboard_logout, name="logout"),

    path('diller_list/', dillers_list,name="dillers"),
    path('diller_delete/', diller_delete,name="dillers"),
    ]