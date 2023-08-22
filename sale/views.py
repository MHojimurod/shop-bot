from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from sale.models import CashOrder, SaleSeller, Card, Cashback

def cash_orders(request):
    orders = CashOrder.objects.order_by("-id").all()
    return render(request, 'dashboard/sale/cash_orders.html', {'orders': orders})

def update_cash_order(request,pk, state):
    order = CashOrder.objects.get(pk=pk)
    order.state = state
    if state == 2:
        order.seller.account-= order.price
        order.seller.save()
    order.save()
    return redirect("cash_orders")
    


def sale_seller(request):
    seller = SaleSeller.objects.order_by("-id").exclude(state=0).all()
    ctx ={
        "seller":seller
    }
    return render(request, 'dashboard/sale/seller.html',ctx)


def update_sale_seller(request, pk, state):
    seller = SaleSeller.objects.get(pk=pk)
    seller.state = state
    seller.save()
    return redirect("sale_seller")

def wait_cashback(request):
    wait = Cashback.objects.order_by("-id").filter(state=1)
    ctx = {
        "wait":wait
    }
    return render(request, 'dashboard/sale/cashback_wait.html', ctx)

def accept_cashback(request):
    accept = Cashback.objects.order_by("-id").filter(state=2)
    ctx = {
        "accept":accept
    }
    return render(request, 'dashboard/sale/cashback_accept.html', ctx)

def reject_cashback(request):
    reject = Cashback.objects.order_by("-id").filter(state=3)
    ctx = {
        "reject":reject
    }
    return render(request, 'dashboard/sale/cashback_reject.html', ctx)

def update_cashback(request,pk, state):
    cashback = Cashback.objects.get(pk=pk)
    cashback.state = state
    cashback.save()
    if state == 3:
        cashback.seria.is_used = False
        cashback.seria.seller.account -= cashback.seria.cashback
        cashback.seria.save()
        cashback.seria.seller.save()
    return redirect("wait_cashback")