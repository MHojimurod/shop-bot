from os import name
from django.urls import path

import diller
from .views import *


urlpatterns = [
    # path('',home, name="home"),
    path('', dillers_list,name="home"),
    path('sellers_list/', sellers_list,name="sellers_list"),
    path('login/', dashboard_login, name="login"),
    path('logout/', dashboard_logout, name="logout"),

    path('diller_update/<int:pk>/<int:status>/', diller_update,name="diller_update"),
    path('diller_delete/<int:pk>/', diller_delete,name="diller_delete"),
    path('seller_delete/<int:pk>/', seller_delete,name="seller_delete"),
    ]