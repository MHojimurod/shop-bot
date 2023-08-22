from django.urls import path
from sale.views import cash_orders, update_cash_order, sale_seller,update_sale_seller, wait_cashback, accept_cashback, reject_cashback, update_cashback
urlpatterns = [
    path('cash/orders', cash_orders, name="cash_orders"),
    path('cash/orders/update/<int:pk>/<int:state>', update_cash_order, name="update_cash_orders"),
    path('sale/seller', sale_seller, name="sale_seller"),
    path('sale/seller/update/<int:pk>/<int:state>', update_sale_seller, name="update_sale_seller"),

    path('cashback/wait', wait_cashback, name="wait_cashback"),
    path('cashback/accept', accept_cashback, name="accept_cashback"),
    path('cashback/reject', reject_cashback, name="reject_cashback"),
    path('cashback/update/<int:pk>/<int:state>', update_cashback, name="update_cashback"),
]