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
    
    
    path('gifts/', gifts,name="gifts"),
    path('gift_create/', gift_create,name="gift_create"),
    path('gift_edit/<int:pk>', gift_edit,name="gift_edit"),
    path('gift_delete/<int:pk>/', gift_delete,name="gift_delete"),


    path('regions/', regions,name="regions"),
    path('region_create', region_create,name="region_create"),
    path('region_edit/<int:pk>/', region_edit,name="region_edit"),
    path('region_delete/<int:pk>/', region_delete,name="region_delete"),


    path('districts/<int:region_id>', districts,name="districts"),
    path('district_create/<int:pk>', district_create,name="district_create"),
    path('district_edit/<int:pk>/<int:region_id>', district_edit,name="district_edit"),
    path('district_delete/<int:pk>/', district_delete,name="district_delete"),


    path('settings/', settings,name="settings"),
    path('settings_edit/<int:pk>/', settings_edit,name="settings_edit"),

    path('orders/', orders,name="orders"),
    path('update_order/<int:pk>/<int:status>', update_order,name="update_order"),


    path('solds/', solds,name="solds"),
    path('sold_create/', sold_create,name="sold_create"),


    path('prompts/', promotion,name="prompts"),
    path('prompt_create/', prompt_create,name="prompt_create"),
    path('send_req/<int:pk>', send_req,name="send_req"),
    path('del_prompt/<int:pk>', del_prompt,name="del_prompt"),
    ]