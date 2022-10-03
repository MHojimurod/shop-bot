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
    path('seller_update/<int:pk>/<int:status>/', seller_update,name="seller_update"),
    path('diller_delete/<int:pk>/', diller_delete,name="diller_delete"),
    path('seller_delete/<int:pk>/', seller_delete,name="seller_delete"),
    path('diller_create', diller_create,name="diller_create"),

    path('checks', checks,name="checks"),
    path('reject_check/<str:seria>/<int:user>/<int:status>', reject_check,name="update_check"),



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
    path('order_gift/', order_gift,name="order_gift"),
    path('update_gift/<int:pk>/<int:status>/<int:type_order>', update_gift,name="update_gift"),


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
    path('send_orders/', send_orders,name="send_orders"),
    path('update_ball/<int:pk>/<int:varranty>', update_ball,name="update_ball"),
    path('update_order/<int:pk>/<int:status>', update_order,name="update_order"),


    path('solds/', solds,name="solds"),
    path('diller_sold/<int:pk>/', diller_sold,name="diller_sold"),
    path('series/<str:strs>/<int:pk>', series,name="series"),
    path('serial_delete/<int:pk>', serial_delete,name="serial_delete"),
    path('sold_create/', sold_create,name="sold_create"),


    path('prompts/', promotion,name="prompts"),
    path('promotion_order/', promotion_order,name="promotion_order"),
    path('update_prompt/<int:pk>/<int:status>', update_prompt,name="update_prompt"),
    path('prompt_create/', prompt_create,name="prompt_create"),
    path('send_req/<int:pk>', send_req,name="send_req"),
    path('del_prompt/<int:pk>', del_prompt,name="del_prompt"),


    path('reports', reports,name="reports"),

    path("api/all/sellers",get_alla_seller_on_json),
    path("write_text",write_text),
    path("get-seller-data/<int:pk>",seller_excel,name="seller_excel"),
    path("get_district/<int:pk>",get_district),
    path("get_sell/<int:pk>",get_sell)
    ]