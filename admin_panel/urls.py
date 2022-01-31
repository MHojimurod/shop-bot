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
    path('diller_delete/<int:pk>/', diller_delete,name="diller_delete"),
    path('checks', checks,name="checks"),



    path('categories/', categories,name="categories"),
    path('category_create', category_create,name="category_create"),
    path('category_edit/<int:pk>/', category_edit,name="category_edit"),
    path('category_delete/<int:pk>/', category_delete,name="category_delete"),


    path('products/<int:category_id>', products,name="products"),
    path('product_create/<int:pk>', product_create,name="product_create"),
    path('product_edit/<int:pk>/<int:category_id>', product_edit,name="product_edit"),
    path('product_delete/<int:pk>/', product_delete,name="product_delete"),
    ]