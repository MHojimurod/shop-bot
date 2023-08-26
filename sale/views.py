from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import requests
from telegram.ext import Updater
from sale.models import CashOrder, SaleSeller, Card, Cashback

def cash_orders(request):
    orders = CashOrder.objects.order_by("-id").all()
    return render(request, 'dashboard/sale/cash_orders.html', {'orders': orders, "e_o": "active"})

def update_cash_order(request,pk, state):
    order = CashOrder.objects.get(pk=pk)
    order.state = state
    if state == 2:
        text = {
            "uz": f"Sizning kartangizga  ${order.price} miqdorida pul o'tkazildi",
            "ru": f"С вашей карты было списано {order.price} долларов США.",
        }
        send_message(order.seller.chat_id, text[order.seller.language])
    else:
        order.seller.account+= order.price
        order.seller.save()
        text = {
            "uz": f"Sizning ${order.price} miqdorida pul yechish so'rovingiz bekor qilindi",
            "ru": f"Ваш запрос на вывод средств на сумму ${order.price} был отменен.",
        }
        send_message(order.seller.chat_id, text[order.seller.language])

    order.save()
    return redirect("cash_orders")
    


def sale_seller(request):
    seller = SaleSeller.objects.order_by("-id").exclude(state=0).all()
    ctx ={
        "seller":seller,
        "e_s": "active"
    }
    return render(request, 'dashboard/sale/seller.html',ctx)


def update_sale_seller(request, pk, state):
    seller = SaleSeller.objects.get(pk=pk)
    seller.state = state
    seller.save()
    if state == 2:
        text = {
            "uz": f"Siz qabul qilindingiz boshlash uchun /start buyrug'ini yuboring",
            "ru": f"Вы приняты. Отправьте команду /start для запуска.",
        }
        send_message(seller.chat_id, text[seller.language])
    else:
        text = {
            "uz": f"Sizning so'rovingiz bekor qilindi",
            "ru": f"Ваш запрос отменен",
        }
        send_message(seller.chat_id, text[seller.language])

    return redirect("sale_seller")

def wait_cashback(request):
    wait = Cashback.objects.order_by("-id").filter(state=1)
    ctx = {
        "wait":wait,
        "e_c": "active"
    }
    return render(request, 'dashboard/sale/cashback_wait.html', ctx)

def accept_cashback(request):
    accept = Cashback.objects.order_by("-id").filter(state=2)
    ctx = {
        "accept":accept,
        "e_c": "active"
    }
    return render(request, 'dashboard/sale/cashback_accept.html', ctx)

def reject_cashback(request):
    reject = Cashback.objects.order_by("-id").filter(state=3)
    ctx = {
        "reject":reject,
        "e_c": "active"
    }
    return render(request, 'dashboard/sale/cashback_reject.html', ctx)

def update_cashback(request,pk, state):
    cashback = Cashback.objects.get(pk=pk)
    cashback.state = state
    cashback.save()
    if state == 3:
        cashback.seria.is_used = False
        cashback.seria.save()
        cashback.seria.seller.save()
        text = {
            "uz": f"Siz yuborgan {cashback.seria.code} seria nomer tasdiqdan o'tmadi⚠️",
            "ru": f"Отправленный вами серийный номер {cashback.seria.code} не подтвержден⚠️",
        }
        send_message(cashback.seria.seller.chat_id, text[cashback.seria.seller.language])
    else:
        cashback.seria.seller.account += cashback.seria.cashback
        cashback.seria.seller.save()
        text = {
            "uz": f"Siz yuborgan {cashback.seria.code} seria nomer tasdiqlandi✅",
            "ru": f"Отправленный вами серийный номер {cashback.seria.code} подтвержден✅",
        }
        send_message(cashback.seria.seller.chat_id, text[cashback.seria.seller.language])

    return redirect("wait_cashback")



def send_message(chat_id, message):
    try:
        # bot = Updater("6525921476:AAHn9ocU5-ik7TMuFScvpAw6BAlJwrpywkI")
        # bot.bot.send_message(chat_id=chat_id, message=message)
        res = requests.get(f"https://api.telegram.org/bot6525921476:AAHn9ocU5-ik7TMuFScvpAw6BAlJwrpywkI/sendMessage?text={message}&chat_id={chat_id}")
        print(res.json()['ok'])

    except:
        print("not send message")