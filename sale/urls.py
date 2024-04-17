from django.urls import path
from sale.views import cash_orders, promocode_requests_accept, promocode_requests_reject, promocodes_create, sale_diller_delete, sale_diller_detail, sale_dillers_create, update_cash_order, sale_seller, update_sale_seller, wait_cashback, accept_cashback, reject_cashback, update_cashback, sale_statistics
from sale.views import promocodes, promocodes_create_xlsx, promocodes_edit, promocodes_delete
from sale.views import cars, cars_create, cars_edit, cars_delete, promocodes_check, give_to_diller
from sale.views import sale_seller_edit
from sale.views import (
    promocode_requests,
    promocode_requests_edit,
    # promocode_requests_accept,
    # promocode_requests_reject
)
from sale.views import (
    sale_seller2,
    sale_seller2_edit,
    update_sale_seller2
)

from sale.views import sale_dillers


urlpatterns = [
    path('cash/orders', cash_orders, name="cash_orders"),
    path('cash/orders/update/<int:pk>/<int:state>',
         update_cash_order, name="update_cash_orders"),
    path('sale/seller', sale_seller, name="sale_seller"),
    path('sale/seller/<int:pk>', sale_seller_edit, name="seller_edit"),
    path('sale/seller/update/<int:pk>/<int:state>',
         update_sale_seller, name="update_sale_seller"),


    path('cashback/wait', wait_cashback, name="wait_cashback"),
    path('cashback/accept', accept_cashback, name="accept_cashback"),
    path('cashback/reject', reject_cashback, name="reject_cashback"),
    path('cashback/update/<int:pk>/<int:state>',
         update_cashback, name="update_cashback"),

    path('sale/statistics/<int:pk>', sale_statistics, name="statistics"),



    path('promocodes/', promocodes, name="promocodes"),
    path('promocodes/<int:pk>', promocodes_edit, name="promocodes-edit"),
    path('promocodes/delete/<int:pk>',
         promocodes_delete, name="promocodes-delete"),
    path('promocodes/create', promocodes_create, name="promocode-create"),
    path('promocodes/create_xlsx', promocodes_create_xlsx,
         name="promocode-create-xlsx"),
    path('promocodes/check/<str:seria>',
         promocodes_check, name="promocode-check"),
    path('promocodes/give_to_diller', give_to_diller,
         name="promocode-give_to_diller"),



    path('cars/', cars, name="cars"),
    path('cars/<int:pk>', cars_edit, name="cars-edit"),
    path('cars/delete/<int:pk>', cars_delete, name="cars-delete"),
    path('cars/create', cars_create, name="cars-create"),




    path('cars/create', cars_create, name="cars-create"),




    path('promocode_requests/', promocode_requests, name="promocode-requests"),
    path('promocode_requests/<int:pk>', promocode_requests_edit,
         name="promocode-request-edit"),
    path('promocode_requests/<int:pk>', promocode_requests_edit,
         name="promocode-request-delete"),

    path('promocode_requests/accept', promocode_requests,
         name="promocode-request-accept"),
    path('promocode_requests/<int:pk>/accept',
         promocode_requests_accept, name="promocode-request-accept"),
    path('promocode_requests/<int:pk>/reject',
         promocode_requests_reject, name="promocode-request-reject"),





    path('sale_dillers/', sale_dillers, name="sale_dillers"),
    path('sale_dillers/create', sale_dillers_create, name="sale_dillers_create"),
    path('sale_dillers/<int:pk>/', sale_diller_detail, name="sale_diller_detail"),
    path('sale_dillers/<int:pk>/delete',
         sale_diller_delete, name="sale_diller_delete"),





    path('sale/seller2', sale_seller2, name="sale_seller2"),
    path('sale/seller2/<int:pk>', sale_seller2_edit, name="seller_edit2"),
    path('sale/seller2/update/<int:pk>/<int:state>',
         update_sale_seller2, name="update_sale_seller2"),


]
