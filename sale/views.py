from collections import defaultdict
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import requests
from telegram.ext import Updater
from admin_panel.views import login_required_decorator
from diller.models import Diller
from sale.forms import PromoCodeForm
from sale.models import Car, CashOrder, PromoCode, PromocodeRequest, SaleDiller, SaleSeller, Card, Cashback, SaleSeller2, SerialNumbers
import xlsxwriter
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Ensure this is the correct path to your form
from .forms import CarForm, PromoCodeForm, PromocodeRequestForm, SaleDillerForm, SaleDillerForm, SaleSeller2Form, SaleSellerForm
# from .models import PromoCode, Diller, Car  # Adjust the import paths as necessary
import pandas as pd
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.db.models.query import Q
from django.db.models import Q
from django.utils.timezone import now


@login_required_decorator
def cash_orders(request):
    orders = CashOrder.objects.order_by("-id").all()
    return render(request, 'dashboard/sale/cash_orders.html', {'orders': orders, "e_o": "active"})


@login_required_decorator
def update_cash_order(request, pk, state):
    order = CashOrder.objects.get(pk=pk)
    order.state = state
    if state == 2:
        text = {
            "uz": f"Sizning kartangizga  ${order.price} miqdorida pul o'tkazildi",
            "ru": f"С вашей карты было списано {order.price} долларов США.",
        }
        send_message(order.seller.chat_id, text[order.seller.language])
    else:
        order.seller.account += order.price
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
    ctx = {
        "seller": seller,
        "e_s": "active"
    }
    return render(request, 'dashboard/sale/seller.html', ctx)


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
        "wait": wait,
        "e_c": "active"
    }
    return render(request, 'dashboard/sale/cashback_wait.html', ctx)


@login_required_decorator
def accept_cashback(request):
    accept = Cashback.objects.order_by("-id").filter(state=2)
    ctx = {
        "accept": accept,
        "e_c": "active"
    }
    return render(request, 'dashboard/sale/cashback_accept.html', ctx)


@login_required_decorator
def reject_cashback(request):
    reject = Cashback.objects.order_by("-id").filter(state=3)
    ctx = {
        "reject": reject,
        "e_c": "active"
    }
    return render(request, 'dashboard/sale/cashback_reject.html', ctx)


@login_required_decorator
def update_cashback(request, pk, state):
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
        send_message(cashback.seria.seller.chat_id,
                     text[cashback.seria.seller.language])
    else:
        cashback.seria.seller.account += cashback.seria.cashback
        cashback.seria.seller.save()
        text = {
            "uz": f"Siz yuborgan {cashback.seria.code} seria nomer tasdiqlandi✅",
            "ru": f"Отправленный вами серийный номер {cashback.seria.code} подтвержден✅",
        }
        send_message(cashback.seria.seller.chat_id,
                     text[cashback.seria.seller.language])

    return redirect("wait_cashback")


def send_message(chat_id, message):
    try:
        # bot = Updater("6525921476:AAHn9ocU5-ik7TMuFScvpAw6BAlJwrpywkI")
        # bot.bot.send_message(chat_id=chat_id, message=message)
        res = requests.get(
            f"https://api.telegram.org/bot6525921476:AAHn9ocU5-ik7TMuFScvpAw6BAlJwrpywkI/sendMessage?text={message}&chat_id={chat_id}")
        print(res.json()['ok'])

    except:
        print("not send message")


@login_required_decorator
def sale_statistics(request, pk):
    seller = SaleSeller.objects.get(pk=pk)
    numbers = SerialNumbers.objects.order_by("-id").filter(seller=seller)

    workbook: xlsxwriter.Workbook = xlsxwriter.Workbook(
        f"media/{datetime.now().date()}.xlsx")
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
        worksheet.write(
            f'B{count}', f"{i.used_time.strftime('%d-%m-%Y') if i.used_time else ''}")
        worksheet.write(f'C{count}', f"{i.code}")
        worksheet.write(f'D{count}', f"{i.cashback}")

        count += 1
        forloop += 1
    workbook.close()
    response = HttpResponse(open(workbook.filename, "rb"),
                            content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename={}'.format(
        f"{datetime.now().date()}.xlsx")
    return response


@login_required
def promocodes(request):
    search_query = request.GET.get('search', '')

    queryset = PromoCode.objects.prefetch_related("car", "diller").all()

    if search_query:
        parts = search_query.split()
        q_objects = Q()

        for part in parts:
            # For numeric parts, attempt to filter by order and code, but catch ValueError if conversion fails
            try:
                numeric_part = int(part)
                q_objects |= Q(order=numeric_part) | Q(code=numeric_part)
            except ValueError:
                pass  # Part wasn't numeric, skip to text-based filtering

            # Text-based filtering for car name, letter, and potentially diller name if applicable
            q_objects |= Q(car__name__icontains=part) | Q(
                letter__iexact=part.lower()) | Q(seria__iexact=part.lower())

            # If your Diller model has a name field or similar, include it in the search
            # q_objects |= Q(diller__name__icontains=part)

        queryset = queryset.filter(q_objects)

    return render(request, 'dashboard/promocodes/list.html', {'promocodes': queryset, "b_active_2": "menu-open", "promocodes_navbar": "active"})


@login_required_decorator
def promocodes_create(request):
    model = PromoCode()
    form = PromoCodeForm(request.POST, request.FILES, instance=model)

    if form.is_valid():
        data = form.save()
        return redirect(f"/promocodes")

    ctx = {
        "form": form,
        "b_active_2": "menu-open",
        "promocodes_navbar": "active"
    }
    return render(request, "dashboard/promocodes/form.html", ctx)


@login_required
def promocodes_delete(request, pk: int):
    promo = get_object_or_404(PromoCode, pk=pk)
    promo.delete()
    messages.success(request, 'Promocode deleted successfully.')
    return redirect('promocodes')


@login_required
def promocodes_edit(request, pk: int):
    promo = get_object_or_404(klass=PromoCode, pk=pk)
    if request.method == "POST":
        form = PromoCodeForm(request.POST, instance=promo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Promocode updated successfully.')
            return redirect('promocodes')  # Redirect to the car listing page
    else:
        form = PromoCodeForm(instance=promo)

    return render(request, 'dashboard/promocodes/edit.html', {'form': form, "b_active_2": "menu-open", "promocodes_navbar": "active"})


@login_required
def promocodes_create_xlsx(request):
    if request.method == "POST" and 'xlsxFile' in request.FILES:
        excel_file = request.FILES['xlsxFile']
        try:
            df = pd.read_excel(excel_file)
            if not all(column in df.columns for column in ['seria', 'letter', 'car', 'code']):
                raise ValueError(
                    "The uploaded file does not have the required columns.")

            # Convert car names in the DataFrame to lower case for case-insensitive processing
            df['car'] = df['car'].str.lower()
            df['letter'] = df['letter'].str.lower()

            car_letter_distributions = defaultdict(lambda: defaultdict(list))

            for _, row in df.iterrows():
                # Append seria and code, keeping letter and car name lowercased
                car_letter_distributions[row['car']][row['letter']].append(
                    (row['seria'], row['code']))

            with transaction.atomic():
                for car_lower, letters in car_letter_distributions.items():
                    # Fetch the Car instance case-insensitively
                    car_instance = Car.objects.filter(
                        name__iexact=car_lower).first()
                    if not car_instance:
                        continue  # Skip if the car is not found

                    for letter_lower, entries in letters.items():
                        # Count occurrences of the letter in the car's name, case-insensitively
                        letter_occurrences = car_instance.name.lower().count(letter_lower)
                        if letter_occurrences == 0:
                            continue  # Skip if the letter does not occur in the car's name

                        # Generate order values based on occurrences within the Excel file
                        orders = [i % letter_occurrences +
                                  1 for i in range(len(entries))]

                        for (seria, code), order in zip(entries, orders):
                            PromoCode.objects.create(
                                car=car_instance,
                                seria=seria,
                                letter=letter_lower,
                                code=code,
                                order=order,
                            )

            messages.success(
                request, "All promo codes were successfully added.")
        except Exception as e:
            messages.error(request, f"Failed to add promo codes. Error: {e}")

        return redirect("/promocodes")

    return render(request, "dashboard/promocodes/form.html", {"b_active_2": "menu-open", "promocodes_navbar": "active"})


@login_required_decorator
def cars(request):

    ctx = {
        "cars": Car.objects.all(),
        "b_active_2": "menu-open",
        "cars_active": "active"
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
        "form": form,
        "b_active_2": "menu-open",
        "cars_active": "active"
    }
    return render(request, "dashboard/cars/form.html", ctx)


@login_required
def cars_delete(request, pk: int):
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    messages.success(request, 'Car deleted successfully.')
    return redirect('cars')


@login_required
def cars_edit(request, pk: int):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car updated successfully.')
            return redirect('cars')  # Redirect to the car listing page
    else:
        form = CarForm(instance=car)

    return render(request, 'dashboard/cars/edit.html', {'form': form,
                                                        "b_active_2": "menu-open", "cars_active": "active"})


@login_required
def promocodes_check(request, seria):
    if request.method == 'GET':  # or 'POST', depending on your preference
        try:
            promocode = PromoCode.objects.get(seria=seria)
            # Perform your check here. This is a placeholder condition.
            # Assuming 'is_valid' is a model field or a method to check validity.
            if promocode.diller == None:
                response = {'status': 'success',
                            'message': 'Promocode is valid.'}
            else:
                response = {'status': 'error',
                            'message': 'Promocode is not valid.'}
        except PromoCode.DoesNotExist:
            response = {'status': 'error',
                        'message': 'Promocode does not exist.'}
        return JsonResponse(response)


@login_required
def give_to_diller(request):
    if request.method == 'POST':
        print(request.POST)
        promocodes: str = request.POST.get('promocode')
        diller_id = request.POST.get('diller')

        # Check if promocodes are provided
        if not promocodes:
            messages.error(request, "No promocodes provided.")
            # Adjust the redirect as needed
            return redirect('sale_diller_detail', diller_id)

        # Attempt to retrieve the Diller object
        try:
            diller = SaleDiller.objects.get(id=diller_id)
        except SaleDiller.DoesNotExist:
            messages.error(request, "Invalid Diller ID.")
            # Adjust the redirect as needed
            return redirect('sale_diller_detail', diller_id)

        # If both checks pass, proceed to update the promocodes
        print(promocodes.replace("\r", "").split("\n"))
        promos = PromoCode.objects.filter(
            seria__in=promocodes.replace("\r", "").split("\n"), diller=None)
        print(promos)
        print(diller)
        promos.update(diller=diller, status=2)

        # Optionally, provide a success message
        messages.success(
            request, f"Promocodes successfully assigned to {diller.name}.")
        # Adjust the redirect as needed
        return redirect('sale_diller_detail', diller_id)
    else:
        # Handle the case for GET or other methods if necessary
        # Adjust the redirect as needed
        return redirect('sale_diller_detail', diller_id)


@login_required
def sale_seller_edit(request, pk: int):
    car = get_object_or_404(SaleSeller, pk=pk)
    if request.method == "POST":
        form = SaleSellerForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'SaleSeller updated successfully.')
            return redirect('cars')  # Redirect to the car listing page
    else:
        form = SaleSellerForm(instance=car)

    return render(request, 'dashboard/sale/seller_edit.html', {'form': form, "b_active_2": "menu-open"})


@login_required_decorator
def promocode_requests(request):

    ctx = {
        "requests": PromocodeRequest.objects.all(),
        "b_active_2": "menu-open",
        "promocodes_request_navbar": "active"
    }
    return render(request, 'dashboard/promocode_requests/list.html', ctx)


@login_required
def promocode_requests_edit(request, pk: int):
    promo_request = get_object_or_404(PromocodeRequest, pk=pk)
    if request.method == "POST":
        form = PromocodeRequestForm(request.POST, instance=promo_request)
        if form.is_valid():
            form.save()
            messages.success(
                request, message='promoCodeRequest updated successfully.')
            # Redirect to the car listing page
            return redirect('promocode-requests')
    else:
        form = PromocodeRequestForm(instance=promo_request)

    # gift_text = promo_request.promo.gifts_text_seller(request=promo_request)

    return render(request, 'dashboard/promocode_requests/edit.html', {'form': form, "b_active_2": "menu-open", "promocodes_request_navbar": "active"})


@login_required
def promocode_requests_accept(request, pk: int):
    promo_request = PromocodeRequest.objects.get(pk=pk)

    promo_request.status = 2
    promo_request.changed_at = now()

    promo_request.save()

    # promo = promo_request.promo

    # promo.status = 3
    # promo.seller = promo_request.seller

    # promo.image = promo_request.image

    # promo.give_promo(promo_request, promo_request.seller)

    print("salom")

    return redirect('promocode-requests',)


@login_required
def promocode_requests_reject(request, pk: int):
    promo_request = PromocodeRequest.objects.get(pk=pk)

    promo_request.status = 3
    promo_request.changed_at = now()
    promo_request.save()


    promo = promo_request.promo
    promo.status = 2
    promo.seller = None
    promo.image = None
    promo.save()

    return redirect('promocode-requests')


@login_required_decorator
def sale_dillers(request):

    ctx = {
        "dillers": SaleDiller.objects.all(),
        "b_active_2": "menu-open",
        "sale_dillers_navbar": "active"
    }
    return render(request, 'dashboard/sale_diller/list.html', ctx)


@login_required_decorator
def sale_dillers_create(request):
    model = SaleDiller()
    form = SaleDillerForm(request.POST, request.FILES, instance=model)

    if form.is_valid():
        data = form.save()
        return redirect(f"/sale_dillers")

    ctx = {
        "form": form,
        "b_active_2": "menu-open",
        "sale_dillers_navbar": "active"
    }
    return render(request, "dashboard/sale_diller/form.html", ctx)


@login_required_decorator
def sale_diller_detail(request, pk: int):
    diller = get_object_or_404(SaleDiller, pk=pk)
    if request.method == "POST":
        form = SaleDillerForm(request.POST, instance=diller)
        if form.is_valid():
            form.save()
            messages.success(
                request, message='promoCodeRequest updated successfully.')
            # Redirect to the car listing page
            return redirect('promocode-requests')
    else:
        form = SaleDillerForm(instance=diller)

    # gift_text = promo_request.promo.gifts_text_seller(request=promo_request)

    return render(
        request,
        'dashboard/sale_diller/edit.html',
        {
            'form': form,
            "b_active_2": "menu-open",
            "sale_diller_navbar": "active",
            'promocodes': diller.promocodes.all()
        }
    )





@login_required
def sale_diller_delete(request, pk: int):
    dillers = get_object_or_404(SaleDiller, pk=pk)
    dillers.delete()
    messages.success(request, 'SaleDiller deleted successfully.')
    return redirect('sale_dillers')















@login_required_decorator
def sale_seller2(request):
    seller = SaleSeller2.objects.order_by("-id").exclude(state=0).all()
    ctx = {
        "seller": seller,
        "e_s2": "active"
    }
    return render(request, 'dashboard/sale2/seller.html', ctx)


@login_required_decorator
def update_sale_seller2(request, pk, state):
    seller = SaleSeller2.objects.get(pk=pk)
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

    return redirect("sale_seller2")



@login_required
def sale_seller2_edit(request, pk: int):
    car = get_object_or_404(SaleSeller2, pk=pk)
    if request.method == "POST":
        form = SaleSeller2Form(request.POST, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'SaleSeller updated successfully.')
            return redirect('sale_seller2')  # Redirect to the car listing page
    else:
        form = SaleSellerForm(instance=car)

    return render(request, 'dashboard/sale2/seller_edit.html', {'form': form, "b_active_2": "menu-open"})
