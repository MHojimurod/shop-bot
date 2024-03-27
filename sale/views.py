from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import requests
from telegram.ext import Updater
from admin_panel.views import login_required_decorator
from sale.forms import PromoCodeForm
from sale.models import Car, CashOrder, PromoCode, SaleSeller, Card, Cashback, SerialNumbers
import xlsxwriter
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CarForm, PromoCodeForm  # Ensure this is the correct path to your form
# from .models import PromoCode, Diller, Car  # Adjust the import paths as necessary
import pandas as pd
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



@login_required_decorator
def cash_orders(request):
    orders = CashOrder.objects.order_by("-id").all()
    return render(request, 'dashboard/sale/cash_orders.html', {'orders': orders, "e_o": "active"})


@login_required_decorator
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



@login_required_decorator
def sale_seller(request):
    seller = SaleSeller.objects.order_by("-id").exclude(state=0).all()
    ctx ={
        "seller":seller,
        "e_s": "active"
    }
    return render(request, 'dashboard/sale/seller.html',ctx)



@login_required_decorator
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


@login_required_decorator
def wait_cashback(request):
    wait = Cashback.objects.order_by("-id").filter(state=1)
    ctx = {
        "wait":wait,
        "e_c": "active"
    }
    return render(request, 'dashboard/sale/cashback_wait.html', ctx)


@login_required_decorator
def accept_cashback(request):
    accept = Cashback.objects.order_by("-id").filter(state=2)
    ctx = {
        "accept":accept,
        "e_c": "active"
    }
    return render(request, 'dashboard/sale/cashback_accept.html', ctx)


@login_required_decorator
def reject_cashback(request):
    reject = Cashback.objects.order_by("-id").filter(state=3)
    ctx = {
        "reject":reject,
        "e_c": "active"
    }
    return render(request, 'dashboard/sale/cashback_reject.html', ctx)


@login_required_decorator
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


@login_required_decorator
def sale_statistics(request,pk):
    seller = SaleSeller.objects.get(pk=pk)
    numbers = SerialNumbers.objects.order_by("-id").filter(seller=seller)

    workbook: xlsxwriter.Workbook = xlsxwriter.Workbook(f"media/{datetime.now().date()}.xlsx")
    worksheet = workbook.add_worksheet()
    worksheet.write(f'A1', f"Sotuvchi")
    worksheet.write(f'B1', f"{seller.name}")
    worksheet.write(f'A3', f"№")
    worksheet.write(f'B3', f"Sana")
    worksheet.write(f'C3', f"Seria nomer")
    worksheet.write(f'D3', f"Cashback")
    count = 4
    forloop = 1
    for i in numbers:
        worksheet.write(f'A{count}', f"{forloop}")
        worksheet.write(f'B{count}', f"{i.used_time.strftime('%d-%m-%Y') if i.used_time else ''}")
        worksheet.write(f'C{count}', f"{i.code}")
        worksheet.write(f'D{count}', f"{i.cashback}")

        count += 1
        forloop += 1
    workbook.close()
    response = HttpResponse(open(workbook.filename, "rb"),
                            content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename={}'.format(f"{datetime.now().date()}.xlsx")
    return response







# @login_required_decorator
# def promocodes(request):

#     ctx = {
#         "promocodes": PromoCode.objects.all()
#     }
#     return render(request, 'dashboard/promocodes/list.html', ctx)

def promocodes(request):
    promocodes_list = PromoCode.objects.all()
    paginator = Paginator(promocodes_list, 10)  # Show 10 promo codes per page

    page_number = request.GET.get('page')
    promo_codes = paginator.get_page(page_number)

    return render(request, 'dashboard/promocodes/list.html', {'promocodes': promo_codes})


@login_required_decorator
def promocodes_create(request):
    model = PromoCode()
    form = PromoCodeForm(request.POST, request.FILES, instance=model)

    if form.is_valid():
        data = form.save()
        return redirect(f"/promocodes")

    ctx = {
        "form": form
    }
    return render(request, "dashboard/promocodes/form.html", ctx)







@login_required
def promocodes_delete(request, pk:int):
    promo = get_object_or_404(PromoCode, pk=pk)
    promo.delete()
    messages.success(request, 'Promocode deleted successfully.')
    return redirect('promocodes')





@login_required
def promocodes_edit(request, pk:int):
    promo = get_object_or_404(klass=PromoCode, pk=pk)
    if request.method == "POST":
        form = PromoCodeForm(request.POST, instance=promo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Promocode updated successfully.')
            return redirect('promocodes')  # Redirect to the car listing page
    else:
        form = PromoCodeForm(instance=promo)

    return render(request, 'dashboard/promocodes/edit.html', {'form': form})






@login_required
def promocodes_create_xlsx(request):
    if request.method == "POST" and 'xlsxFile' in request.FILES:
        excel_file = request.FILES['xlsxFile']
        try:
            df = pd.read_excel(excel_file)
            # Ensuring we have the expected columns in the uploaded Excel file
            expected_columns = ['seria', 'letter', 'car', 'code']
            if not all(column in df.columns for column in expected_columns):
                raise ValueError("The uploaded file does not have the required columns.")

            with transaction.atomic():
                for _, row in df.iterrows():
                    car_name = row['car']  # Assuming this column contains the car's name
                    car_instance = Car.objects.filter(name=car_name).first()
                    if not car_instance:
                        # If a matching car isn't found, raise an error to abort the transaction
                        raise ValueError(f"Car not found for name: {car_name}")

                    # Attempt to create the PromoCode instance
                    PromoCode.objects.create(
                        car=car_instance,
                        seria=row['seria'],
                        letter=row['letter'],
                        code=row['code'],
                    )

            messages.success(request, "All promo codes were successfully added.")
        except Exception as e:
            # If any error occurs, including missing columns or database issues,
            # the transaction will be rolled back, and no promo codes will be added
            messages.error(request, f"Failed to add promo codes. Error: {e}")

        return redirect("/promocodes")

    # If not a POST request or the file is not provided, render the form again
    ctx = {}
    return render(request, "dashboard/promocodes/form.html", ctx)









@login_required_decorator
def cars(request):

    ctx = {
        "cars": Car.objects.all()
    }
    return render(request, 'dashboard/cars/list.html', ctx)



@login_required_decorator
def cars_create(request):
    model = Car()
    form = CarForm(request.POST, request.FILES, instance=model)

    if form.is_valid():
        data = form.save()
        return redirect(f"/cars")

    ctx = {
        "form": form
    }
    return render(request, "dashboard/cars/form.html", ctx)






@login_required
def cars_delete(request, pk:int):
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    messages.success(request, 'Car deleted successfully.')
    return redirect('cars')





@login_required
def cars_edit(request, pk:int):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car updated successfully.')
            return redirect('cars')  # Redirect to the car listing page
    else:
        form = CarForm(instance=car)

    return render(request, 'dashboard/cars/edit.html', {'form': form})
