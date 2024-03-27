from django.urls import path
from sale.views import cash_orders, promocodes_create, update_cash_order, sale_seller,update_sale_seller, wait_cashback, accept_cashback, reject_cashback, update_cashback, sale_statistics
from sale.views import promocodes,promocodes_create_xlsx,promocodes_edit,promocodes_delete
from sale.views import cars, cars_create,cars_edit,cars_delete


urlpatterns = [
    path('cash/orders', cash_orders, name="cash_orders"),
    path('cash/orders/update/<int:pk>/<int:state>', update_cash_order, name="update_cash_orders"),
    path('sale/seller', sale_seller, name="sale_seller"),
    path('sale/seller/update/<int:pk>/<int:state>', update_sale_seller, name="update_sale_seller"),

    path('cashback/wait', wait_cashback, name="wait_cashback"),
    path('cashback/accept', accept_cashback, name="accept_cashback"),
    path('cashback/reject', reject_cashback, name="reject_cashback"),
    path('cashback/update/<int:pk>/<int:state>', update_cashback, name="update_cashback"),

    path('sale/statistics/<int:pk>', sale_statistics, name="statistics"),



    path('promocodes/', promocodes,name="promocodes"),
    path('promocodes/<int:pk>', promocodes_edit,name="promocodes-edit"),
    path('promocodes/delete/<int:pk>', promocodes_delete,name="promocodes-delete"),
    path('promocodes/create', promocodes_create,name="promocode-create"),
    path('promocodes/create_xlsx', promocodes_create_xlsx,name="promocode-create-xlsx"),



    path('cars/', cars,name="cars"),
    path('cars/<int:pk>', cars_edit,name="cars-edit"),
    path('cars/delete/<int:pk>', cars_delete,name="cars-delete"),
    path('cars/create', cars_create,name="cars-create"),
]
