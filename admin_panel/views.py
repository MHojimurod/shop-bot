import datetime
import os
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from admin_panel.forms import CategoryForm, DillerForm, DistrictForm, GiftsForm, ProductForm, PromotionForm, RegionsForm, SoldForm, TextForm
from admin_panel.models import BaseProduct, Gifts, Promotion_Order, Regions, District, Category, Product, Text, Promotion
from diller.models import Diller, Busket, Busket_item, OrderGiftDiller
from seller.models import Cvitation, OrderGiftSeller, Seller
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import requests
from django.db.models import Q
import xlsxwriter
from telegram.ext import Updater
from seller.management.commands.constant import TOKEN
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def money(number: int, grouping: bool = True):
    return f"{locale.currency(number, grouping=grouping).split('.')[0][1:]}"


def login_required_decorator(f):
    return login_required(f, login_url="login")


def dashboard_login(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
    return render(request, "dashboard/login.html")


@login_required_decorator
def dashboard_logout(request):
    logout(request)
    res = redirect("login")
    res.delete_cookie("sessionid")
    return res


@login_required_decorator
def dillers_list(request):
    dillers = Diller.objects.order_by('-id').all()
    ctx = {
        "dillers": dillers,
        "d_active": "menu-open"
    }
    return render(request, "dashboard/diller.html", ctx)


@login_required_decorator
def diller_create(request):
    model = Diller()
    form = DillerForm(request.POST, instance=model)
    if form.is_valid():
        form.instance.status = 1
        form.save()
        return redirect("/")
    return render(request, "dashboard/diller_create.html", {"form": form})


@login_required_decorator
def sellers_list(request):
    sellers = Seller.objects.order_by('-id').all()
    ctx = {
        "sellers": sellers,
        "sel_active": "menu-open"
    }
    return render(request, "dashboard/seller.html", ctx)


@login_required_decorator
def diller_update(request, pk, status):
    Diller.objects.filter(pk=pk).update(status=status)
    try:
        data = requests.get(f"http://127.0.0.1:6002/diller_status", json={"data": {
            "id": pk,
            "status": status
        }})
    except:
        ...
    return redirect("home")


@login_required_decorator
def seller_update(request, pk, status):
    Seller.objects.filter(pk=pk).update(status=status)
    try:
        data = requests.get(f"http://127.0.0.1:6003/seller_status", json={"data": {
            "id": pk,
            "status": status
        }})
    except:
        ...
    return redirect("sellers_list")


@login_required_decorator
def diller_delete(request, pk):
    model = Diller.objects.get(pk=pk)
    model.delete()
    return redirect("home")


@login_required_decorator
def seller_delete(request, pk):
    model = Seller.objects.get(pk=pk)
    try:
        a = requests.get(f"http://127.0.0.1:6003/delete_seller", json={"data": {
            "id": pk,
        }})
        if a.status_code == 500:
            model.delete()
    except:
        ...
    return redirect("sellers_list")


@login_required_decorator
def checks(request):
    wait = Cvitation.objects.order_by(
        "-id").filter(~Q(seller=None), status=0)
    accept = Cvitation.objects.order_by(
        "-id").filter(~Q(seller=None), status=1)
    reject = Cvitation.objects.order_by(
        "-id").filter(~Q(seller=None), status=2)
    ctx = {
        "wait": wait,
        "accept": accept,
        "reject": reject,
        "ch_active": "menu-open"
    }
    return render(request, "dashboard/checks.html", ctx)


@login_required_decorator
def reject_check(requset, seria, user, status):
    print("aaaaaaa")
    cv = Cvitation.objects.filter(serial=seria)
    if status == 2:
        seller = Seller.objects.filter(pk=user)
        seller.update(balls=seller.first().balls - cv.first().current_ball)
        try:
            requests.get(f"http://127.0.0.1:6003/reject_check", json={"data": {
                "id": cv.first().seller.id,
                "serial": seria}})
        except:...
        cv.update(status=status)
        return redirect("checks")
    else:
        cv.update(status=status)
        return redirect("checks")


@login_required_decorator
def categories(request):
    category = Category.objects.all()

    ctx = {
        "categories": category,
        "cat_active": "menu-open"
    }
    return render(request, "dashboard/category/list.html", ctx)


@login_required_decorator
def category_create(request):
    model = Category()
    form = CategoryForm(request.POST, request.FILES, instance=model)
    if form.is_valid():
        form.save()
        return redirect("categories")

    ctx = {
        "form": form,
    }
    return render(request, "dashboard/category/form.html", ctx)


@login_required_decorator
def category_edit(request, pk):
    model = Category.objects.get(pk=pk)
    form = CategoryForm(request.POST or None,
                        request.FILES or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect("categories")
        else:
            print(form.errors)
    ctx = {"form": form}
    return render(request, "dashboard/category/form.html", ctx)


@login_required_decorator
def category_delete(request, pk):
    model = Category.objects.get(pk=pk)
    model.delete()
    return redirect("categories")


@login_required_decorator
def products(request, category_id):
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category_id=category_id)
    ctx = {
        "products": products,
        "category": category,
    }
    return render(request, "dashboard/product/list.html", ctx)


@login_required_decorator
def product_create(request, pk):
    model = Product()
    form = ProductForm(request.POST, request.FILES, instance=model)
    if form.is_valid():
        data = form.save()
        return redirect(f"/products/{data.category_id}")

    ctx = {
        "form": form,
        "pk": pk
    }
    return render(request, "dashboard/product/form.html", ctx)


@login_required_decorator
def product_edit(request, pk, category_id):
    model = Product.objects.get(pk=pk)
    form = ProductForm(request.POST or None,
                       request.FILES or None, instance=model)
    if request.POST:
        if form.is_valid():
            data = form.save()
            return redirect(f"/products/{data.category_id}")
        else:
            print(form.errors)
    ctx = {"form": form,
           "pk": category_id
           }
    return render(request, "dashboard/product/form.html", ctx)


@login_required_decorator
def product_delete(request, pk):
    model = Product.objects.get(pk=pk)
    model.delete()
    return redirect(f"/products/{model.category_id}")


@login_required_decorator
def gifts(request):
    data = Gifts.objects.all()
    ctx = {
        "gifts": data,
        "g_active": "menu-open"
    }
    return render(request, "dashboard/gifts/list.html", ctx)


@login_required_decorator
def gift_create(request):
    model = Gifts()
    form = GiftsForm(request.POST, request.FILES, instance=model)
    if form.is_valid():
        form.save()
        return redirect("gifts")

    ctx = {
        "form": form,
    }
    return render(request, "dashboard/gifts/form.html", ctx)


@login_required_decorator
def gift_edit(request, pk):
    model = Gifts.objects.get(pk=pk)
    form = GiftsForm(request.POST or None,
                     request.FILES or None, instance=model)
    if request.POST:
        if form.is_valid():
            data = form.save()
            return redirect("gifts")
        else:
            print(form.errors)
    ctx = {"form": form}
    return render(request, "dashboard/gifts/form.html", ctx)


@login_required_decorator
def gift_delete(request, pk):
    model = Gifts.objects.get(pk=pk)
    model.delete()
    return redirect("gifts")


@login_required_decorator
def regions(request):
    region = Regions.objects.all()

    ctx = {
        "regions": region,
        "r_active": "menu-open"
    }
    return render(request, "dashboard/region/list.html", ctx)


@login_required_decorator
def region_create(request):
    model = Regions()
    form = RegionsForm(request.POST, request.FILES, instance=model)
    if form.is_valid():
        form.save()
        return redirect("regions")

    ctx = {
        "form": form,
        "r_active": "menu-open"
    }
    return render(request, "dashboard/region/form.html", ctx)


@login_required_decorator
def region_edit(request, pk):
    model = Regions.objects.get(pk=pk)
    form = RegionsForm(request.POST or None,
                       request.FILES or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect("regions")
        else:
            print(form.errors)
    ctx = {"form": form, "r_active": "menu-open"}
    return render(request, "dashboard/region/form.html", ctx)


@login_required_decorator
def region_delete(request, pk):
    model = Regions.objects.get(pk=pk)
    model.delete()
    return redirect("regions")


@login_required_decorator
def districts(request, region_id):
    region = Regions.objects.get(pk=region_id)
    district = District.objects.filter(region_id=region_id)
    ctx = {
        "region": region,
        "districts": district,
        "r_active": "menu-open"
    }
    return render(request, "dashboard/district/list.html", ctx)


@login_required_decorator
def district_create(request, pk):
    model = District()
    form = DistrictForm(request.POST, request.FILES, instance=model)
    if form.is_valid():
        data = form.save()
        return redirect(f"/districts/{data.region_id}")

    ctx = {
        "form": form,
        "pk": pk,
        "r_active": "menu-open"
    }
    return render(request, "dashboard/district/form.html", ctx)


@login_required_decorator
def district_edit(request, pk, region_id):
    model = District.objects.get(pk=pk)
    form = DistrictForm(request.POST or None,
                        request.FILES or None, instance=model)
    if request.POST:
        if form.is_valid():
            data = form.save()
            return redirect(f"/districts/{data.region_id}")
        else:
            print(form.errors)
    ctx = {"form": form,
           "pk": region_id,
           "r_active": "menu-open"
           }
    return render(request, "dashboard/district/form.html", ctx)


@login_required_decorator
def district_delete(request, pk):
    model = District.objects.get(pk=pk)
    model.delete()
    return redirect(f"/districts/{model.region_id}")


@login_required_decorator
def settings(request):
    texts = Text.objects.all()
    ctx = {
        "texts": texts,
        "se_active": "menu-open"
    }
    return render(request, "dashboard/settings/list.html", ctx)


@login_required_decorator
def settings_edit(request, pk):
    model = Text.objects.get(pk=pk)
    form = TextForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect("settings")
    ctx = {
        "form": form
    }
    return render(request, "dashboard/settings/form.html", ctx)


@login_required_decorator
def orders(request):
    busket = Busket.objects.filter(status__in=[0, 1], is_ordered=True)
    data = []
    a = {"total": 0, }
    sub_total = 0
    for i in busket:
        diller = i.diller

        text = ""
        ball = 0
        for j in Busket_item.objects.filter(busket=i):
            text += f"{j.product.name_uz} x <b>{j.count}</b> = {money(j.product.price * j.count)}<br>"
            a["total"] += j.product.price * j.count
            sub_total += j.product.price * j.count
            ball += j.product.diller_ball*j.count

        data.append(
            {
                "id": i.id,
                "diller": diller,
                "text": text,
                "ball": ball,
                "busket": i,
                "sub_total": money(sub_total)
            })
        sub_total = 0
    ctx = {
        "items": data,
        "total": money(a["total"]),
        "dil_active": "active"
    }

    return render(request, "dashboard/order/list.html", ctx)


@login_required_decorator
def send_orders(request):
    busket = Busket.objects.filter(status__in=[2, 4], is_ordered=True)
    data = []
    a = {"total": 0, }
    sub_total = 0
    for i in busket:
        diller = i.diller

        text = ""
        ball = 0
        nasiya_ball = 0
        for j in Busket_item.objects.filter(busket=i):
            text += f"{j.product.name_uz} x <b>{j.count}</b> = {money(j.product.price * j.count)}<br>"
            a["total"] += j.product.price * j.count
            sub_total += j.product.price * j.count
            ball += j.product.diller_ball*j.count
            nasiya_ball += j.product.diller_nasiya_ball*j.count

        data.append(
            {
                "id": i.id,
                "payment_type": i.payment_type,
                "is_purchased": i.is_purchased,
                "diller": diller,
                "text": text,
                "ball": ball,
                "nasiya_ball": nasiya_ball,
                "busket": i,
                "sub_total": money(sub_total)
            })
        sub_total = 0
    ctx = {
        "items": data,
        "total": money(a['total']),
        "dil_active": "active",
        "sol_active": "menu-open"

    }

    return render(request, "dashboard/order/send_orders.html", ctx)


@login_required_decorator
def update_order(request, pk, status):
    data = Busket.objects.filter(pk=pk).update(status=status)
    requests.get("http://127.0.0.1:6002/update_status", json={
        "data": {
            "diller": Busket.objects.filter(pk=pk).first().diller.id,
            "status": status,
            "busket": Busket.objects.filter(pk=pk).first().id

        }
    })
    return redirect("orders")


@login_required_decorator
def solds(request):
    all = BaseProduct.objects.order_by("-id").all()
    data = []
    for i in all.exclude(diller=None):
        if i.diller not in [j['diller'] for j in data if data != []]:
            count = BaseProduct.objects.filter(diller=i.diller).count()
            data.append(
                {"diller": i.diller, "count": count, "seller": i.seller})
    ctx = {
        "baseproduct": data,
        "s_active": "menu-open"
    }
    return render(request, "dashboard/sold/list.html", ctx)


def cout_product(diller: Diller, date: str):
    data = []
    products = []
    if date in ["day", "month", "year"]:
        products = BaseProduct.objects.filter(diller=diller, date__lte=datetime.datetime.today(), date__gt=datetime.datetime.today()-datetime.timedelta(days=(
            1 if date == "day" else (30 if date == "month" else 365)
        )))
    else:
        products = BaseProduct.objects.filter(diller=diller)
    d = {}
    for item in products.exclude(product=None):
        if item.product.id not in d:
            d[item.product.id] = {
                "diller": item.diller,
                "product": item.product,
                "serial_numbers": [item.serial_number],
                "count": 1
            }
        else:
            d[item.product.id]["count"] += 1
            d[item.product.id]['serial_numbers'].append(
                item.serial_number
            )
    return d


@login_required_decorator
def diller_sold(request, pk):
    diller = Diller.objects.filter(id=pk)
    if diller:

        total = 0
        data = cout_product(diller.first(), request.GET.get("filter_product"))
        for j in data.values():
            total += j["product"].price*j['count']
        return render(request, "dashboard/sold/diller_sold.html", {"data": [d for d in data.values()], "total": money(total)})


@login_required_decorator
def series(request, strs, pk):
    products = BaseProduct.objects.filter(product__name_uz=strs, diller_id=pk)
    return render(request, "dashboard/sold/series.html", {"data": products})


@login_required_decorator
def serial_delete(request, pk):
    product: BaseProduct = BaseProduct.objects.filter(pk=pk).first()
    if product:
        res = redirect("series", product.product.name_uz, product.diller.id)
        product.delete()
        return res


def update_ball(request, pk, varranty):
    busket = Busket.objects.filter(pk=pk)
    if busket:
        ball = busket.first().ball_by_var(varranty)
        diller = busket.first().diller
        diller.balls += ball
        diller.save()
        busket.update(is_purchased=True)
        busket.update(payment_type=0 if varranty == 1 else 1)
        return redirect("send_orders")


@login_required_decorator
def sold_create(request):
    model = BaseProduct()
    form = SoldForm(request.POST, instance=model)
    if form.is_valid():
        diller = request.POST["diller"]
        seller = request.POST["seller"]
        product = request.POST["product"]
        req = request.POST["serial2"]
        pr:Product = Product.objects.get(pk=product)
        sl:Seller = Seller.objects.get(pk=seller)
        count = pr.last_code
        # req = request.POST["serial"].strip().replace("\t","").replace("\r","")
        # sers = [i for i in req.split("\n")]
        workbook: xlsxwriter.Workbook = xlsxwriter.Workbook(f"media/{sl.name}.xlsx")
        worksheet = workbook.add_worksheet()
        worksheet.write(f'A1', f"Sotuvchi {seller}")
        worksheet.write(f'B1', sl.name)
        worksheet.write(f'A3', f"№")
        worksheet.write(f'B3', f"{pr.name_uz}")
        count_1 = 4
        for i in range(int(req)):
            count+=1
            worksheet.write(f'A{count_1}', f"{i+1}")
            worksheet.write(f'B{count_1}', f"{pr.code}{count}")
            BaseProduct.objects.create(
                diller_id=diller, product=pr, serial_number=f"{pr.code}{count}", seller_id=seller)
            count_1 +=1
        pr.last_code=count
        pr.save()
        workbook.close()
        open(workbook.filename, "rb")
        data = requests.get(f"http://127.0.0.1:6002/excel", json={"data":workbook.filename })
                          

        return redirect("solds")
    print(form.errors)
    return render(request, "dashboard/sold/form.html", {"form": form})


@login_required_decorator
def promotion(request):
    data = Promotion.objects.all()
    ctx = {
        "prompts": data,
        "pr_active": "menu-open"

    }
    return render(request, "dashboard/promotion/list.html", ctx)


@login_required_decorator
def prompt_create(request):
    model = Promotion()
    form = PromotionForm(request.POST, instance=model)
    if form.is_valid():
        form.save()
        return redirect("prompts")
    else:
        print(form.errors)

    return render(request, "dashboard/promotion/form.html", {"form": form})


@login_required_decorator
def send_req(request, pk):
    data = Promotion.objects.get(pk=pk)
    ctx = {
        "product": data.id
    }
    data = requests.get(f"http://127.0.0.1:6002/send_req", json={"data": ctx})
    return redirect("prompts")


@login_required_decorator
def del_prompt(request, pk):
    data = Promotion.objects.get(pk=pk)
    data.delete()
    return redirect("prompts")


@login_required_decorator
def promotion_order(request):
    data = Promotion_Order.objects.filter(status__in=[0, 1])
    ctx = {
        "data": data,
        "p_active": "active",
        "b_active": "menu-open"
    }
    return render(request, "dashboard/promotion/list1.html", ctx)


@login_required_decorator
def update_prompt(request, pk, status):
    data = Promotion_Order.objects.filter(pk=pk).update(status=status)
    requests.get("http://127.0.0.1:6002/update_status_prompt", json={
        "data": {
            "diller": Promotion_Order.objects.filter(pk=pk).first().user.id,
            "status": status,
            "ball": Promotion_Order.objects.filter(pk=pk).first().promotion.ball,
        }
    })
    return redirect("promotion_order")


@login_required_decorator
def order_gift(request):
    diller: OrderGiftDiller = OrderGiftDiller.objects.all()
    seller: OrderGiftSeller = OrderGiftSeller.objects.all()

    ctx = {
        "diller": diller,
        "seller": seller,
        "gift_active": "active"
    }
    return render(request, "dashboard/gifts/order.html", ctx)


@login_required_decorator
def update_gift(request, pk, status, type_order):
    if type_order == 0:
        gift_D = OrderGiftDiller.objects.filter(pk=pk)
        if status == 3:
            user = gift_D.first().user
            user.balls =user.balls + gift_D.first().gift.ball
            user.save()
            user.refresh_from_db()
        gift_D.update(status=status)
    elif type_order == 1:
        gift_S = OrderGiftSeller.objects.filter(pk=pk)
        if status == 3:
            user = gift_S.first().user
            user.balls =user.balls + gift_S.first().gift.ball
            user.save()
            user.refresh_from_db()
        gift_S.update(status=status)

    return redirect("order_gift")


def product_data():
    products = []
    products = BaseProduct.objects.all()
    d = {}
    x: "list[BaseProduct]" = products.exclude(product=None)
    for item in x:
        if item.product.id not in d:
            d[item.product.id] = {
                "diller": item.diller,
                "product": item.product,
                "serial_numbers": [item.serial_number],
                "count": 1
            }
        else:
            d[item.product.id]["count"] += 1
            d[item.product.id]['serial_numbers'].append(
                item.serial_number
            )
    return d


@login_required_decorator
def reports(request):
    products = []
    products = BaseProduct.objects.all()
    d = {}
    x: "list[BaseProduct]" = products.exclude(product=None)
    for item in x:
        _seller: Cvitation = Cvitation.objects.filter(
            serial=item.serial_number).first()
        seller: Seller = _seller.seller if _seller else None
        if item.product.id not in d:
            d[item.product.id] = {
                "diller": item.diller,
                "product": item.product,
                "serial_numbers": [item.serial_number],
                "count": 1,
                "sellers": {seller.id: {"j": 1}} if seller else {},
            }
        else:
            d[item.product.id]["count"] += 1
            d[item.product.id]['serial_numbers'].append(
                item.serial_number
            )
            if seller:
                if seller.id not in d[item.product.id]['sellers']:
                    d[item.product.id]['sellers'][seller.id] = {
                        "j": 1
                    }
                else:
                    d[item.product.id]['sellers'][seller.id]['j'] += 1

    new_data = []
    for k, v in d.items():
        new_data = []
        for k2, v2 in v['sellers'].items():
            new_data.append(
                {"i": Seller.objects.filter(id=k2).first(), "j": v2['j']})
        v['sellers'] = new_data

    return render(request, "dashboard/report.html", {"data": [i for i in d.values()]})


def get_alla_seller_on_json(request):
    sellers = Seller.objects.all()
    data = []
    for seller in sellers:
        data.append({
            "id": seller.id,
            "name": seller.name,
            "number": seller.number,
            "region": seller.region.uz_data,
            "district": seller.district.uz_data,
            "shop": seller.shop,
            "series": [i.serial for i in Cvitation.objects.filter(seller=seller)]


        })
    return JsonResponse({"data": data}, safe=False)


def write_text(request):
    data = ["reject_check_text",
            "total",
            "you_are_deleted",
            "request_location",
            "incorrect_shop_location",
            "invalid_number",
            "invalid_name",
            "product_count_limit",
            "price",
            "sum",
            "passport_photo",
            "shop_passport_photo",
            "shop_location",
            "wait_accept",
            "menu",
            "cvitation",
            "diller_accept_order",
            "balls",
            "back_btn",
            "add_again_btn",
            "order_btn",
            "add_to_cart",
            "shop_name",
            "seria_not_found",
            "already_sold",
            "cvitation_success",
            "send_cvi_serial_number",
            "send_cvitation",
            "my_balls",
            "buy",
            "taken",
            "not_access",
            "accept_your_prompt",
            "not_enought_balls",
            "no",
            "yes",
            "are_you_sure_get_gift",
            "no_orders",
            "loan",
            "cash",
            "pay_type",
            "empty_busket",
            "promotion_count_error",
            "promotion_count_message",
            "prompt_end",
            "i_bought",
            "reject_message",
            "accept_message",
            "order_denied",
            "order_delivered",
            "order_accepted",
            "language_not_found",
            "region_not_found",
            "district_not_found",
            "select_district",
            "select_region",
            "send_number",
            "request_number",
            "request_name",
            "start",
            "invalid_passport_photo",
            "invalid_shop_passport_photo"]

    for i in data:
        Text.objects.get_or_create(name=i, uz_data=i, ru_data=i)
    return redirect("/")


@login_required_decorator
def seller_excel(request, pk):
    seller = Seller.objects.get(pk=pk)
    cvitation: Cvitation = Cvitation.objects.filter(seller=seller, status=1)
    workbook: xlsxwriter.Workbook = xlsxwriter.Workbook(
        f"media/{seller.name}.xlsx")
    worksheet = workbook.add_worksheet()
    worksheet.write(f'A1', f"Sotuvchi")
    worksheet.write(f'B1', seller.name)
    worksheet.write(f'A3', f"№")
    worksheet.write(f'B3', f"Sana")
    worksheet.write(f'C3', f"Seria Nomerlar")
    worksheet.write(f'D3', f"Sotuvchi Hududi")
    worksheet.write(f'E3', f"Mahsulot nomi")
    worksheet.write(f'F3', f"Berilgan ball")
    count = 4
    forloop = 1
    for i in cvitation:
        product = BaseProduct.objects.filter(serial_number=i.serial)
        worksheet.write(f'A{count}', f"#{forloop}")
        worksheet.write(f'B{count}', f"{i.created_at.strftime('%d-%m-%Y')}")
        worksheet.write(f'C{count}', f"{i.serial}")
        worksheet.write(f'D{count}', f"{i.seller.region.uz_data}")
        worksheet.write(
            f'E{count}', f"{product.first().product.name_uz if product else '' }")
        worksheet.write(
            f'F{count}', f"{product.first().product.seller_ball if product else ''}")
        count += 1
        forloop += 1
    workbook.close()
    response = HttpResponse(open(workbook.filename, "rb"),
                            content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename={}'.format(
        f"{seller.name}_{datetime.datetime.now()}.xlsx")
    return response


def get_district(request, pk):
    districts = District.objects.filter(region_id=pk)
    # data =[{str(i.id):i.uz_data} for i in districts]
    data = {}
    for i in districts:
        data.update({str(i.id): i.uz_data})
    return JsonResponse(data, safe=False)


def get_sell(request, pk):
    districts = Seller.objects.filter(dillers__in=[Diller.objects.get(id=pk)])
    data = {}
    for i in districts:
        data.update({str(i.id): i.name})
    return JsonResponse(data, safe=False)

@login_required_decorator
def write_regions(request):
    data = [{'uz': 'Qoraqalpoq', 'district_uz': ['Amudaryo tumani', 'Beruniy tumani', 'Chimboy tumani', "Ellikqal'a tumani", 'Kegeyli tumani *', 'Mo‘ynoq tumani', 'Nukus tumani', 'Qonliko‘l tumani', 'Qo‘ng‘irot tumani', "Qorao'zak tumani", 'Shumanay tumani', "Taxtako'pir tumani", 'To‘rtko‘l tumani', 'Xo‘jayli tumani', ], 'ru': 'каракалпакский', 'district_ru': ['Амударьинский район', 'Берунийский район', 'Чимбойский район', 'Элликкалинский район', 'Кегейлийский район *', 'Мойнокский район', 'Нукусский район', 'Конлыкольский район', 'Куниратский район', 'Караозакский район', 'Шуманайский район', 'Тахтакорпирский район', 'Торткольский район', 'Ходжалинский район', ]}, {'uz': 'Xorazm', 'district_uz': ["Bog'ot tumani", 'Gurlen tumani', 'Xonqa tumani', 'Hazorasp tumani', 'Xiva tumani', 'Qo‘shko‘pir tumani', 'Shovot tumani', 'Urganch tumani', 'Yangiariq tumani', 'Yangibozor tumani', ], 'ru': 'Хорезм', 'district_ru': ['Боготский район', 'Гурленский район', 'Ханкайский район', 'Хазораспский район', 'Хивинский район', 'Кошкопирский район', 'Шаватский район', 'Ургенчский район', 'Янгарикский район', 'Янгибозарский район', ]}, {'uz': 'Navoiy', 'district_uz': ['Kanimex tumani', 'Navoiy tumani', 'Qiziltepa tumani', 'Xatirchi tumani', 'Navbahor tumani', 'Nurota tumani', 'Tamdi tumani', 'Uchquduq tumani', ], 'ru': 'Навои', 'district_ru': ['Канимехский район', 'Навоийский район', 'Кызылтепинский район', 'Хатырчинский район', 'Навбахорский район', 'Нуратинский район', 'Тамди район', 'Узгудукский район', ]}, {'uz': 'Buxoro', 'district_uz': ['Olot tumani', 'Buxoro tumani', "G'ijduvon tumani", 'Jondor tumani', 'Kogon tumani', "Qorako'l tumani", 'Qorovulbozor tumani', 'Peshku tumani', 'Romitan tumani', 'Shofirkon tumani', 'Vabkent tumani', ], 'ru': 'Бухара', 'district_ru': ['Олотский район', 'Бухарский район', 'Гиждуванский район', 'Жондорский район', 'Когонский район', 'Каракольский район', 'Каровулбазарский район', 'Пешку район', 'Ромитанский район', 'Шафирконский район', 'Вабкентский район', ]}, {'uz': 'Samarqand', 'district_uz': ['Bulung‘ur tumani', 'Ishtixon tumani', 'Jomboy tumani', "Kattaqo'rg'on tumani", "Qo'shrabot tumani", 'Narpay tumani', 'Nurobod tumani', 'Oqdaryo tumani', 'Paxtachi tumani', 'Payariq tumani', "Pastdarg'om tumani", 'Samarqand tumani', 'Toyloq tumani', 'Urgut tumani', ], 'ru': 'Самарканд', 'district_ru': ['Булунгурский район', 'Иштиханский район', 'Джомбойский район', 'Каттакурганский район', 'Хошработский район', 'Нарпайский район', 'Нурабадский район', 'Акдарьинский район', 'Пахтачинский район', 'Пайарикский район', 'Пастдаргомский район', 'Самаркандский район', 'Тойлокский район', 'Ургутский район', ]}, {'uz': 'Qashqadaryo', 'district_uz': ['Chiroqchi tumani ', 'Dehqonobod tumani', "G'uzor tumani", 'Qamashi tumani', 'Qarshi tumani', 'Koson tumani', 'Kasbi tumani', 'Kitob tumani', 'Mirishkor tumani', 'Muborak tumani', 'Nishon tumani', 'Shahrisabz tumani', "Yakkabog'tumani", ], 'ru': 'Кашкадарья', 'district_ru': ['Чиракчинский район', 'Дехканабадский район', 'Гузорский район', 'Камаши район', 'Каршинский район', 'Косонский район', 'Касбинский район', 'Книжный район', 'Миришкорский район', 'Мубаракский район', 'Целевой район', 'Шахрисабзский район', 'Яккабогтумани', ]}, {'uz': 'Surxondaryo', 'district_uz': ['Angor tumani', 'Bandixon tumani', 'Boysun tumani', 'Denov tumani', "Jarqo'rg'on tumani", 'Kizirik tumani', "Qumqo'rg'on tumani", 'Muzrabot tumani', 'Oltinsoy tumani', 'Sariosiyo tumani', 'Sherobod tumani', "Sho'rchi tumani", 'Termiz tumani', 'Uzun tumani', ], 'ru': 'Сурхандарьинская', 'district_ru': ['Ангорский район', 'Бандиханский район', 'Байсунский район', 'Деновский район', 'Джаркурганский район','Кизирикский район', 'Кумкурганский район', 'Музработский район', 'Алтынсойский район', 'Сариосский район', 'Шерабадский район', 'Шорчинский район', 'Термезский район', 'Узунский район', ]}, {'uz': 'Jizzax', 'district_uz': ['Arnasoy tumani', 'Baxmal tumani', "Do'stlik tumani", 'Forish tumani', "G'allaorol tumani", 'Jizzax tumani', "Mirzacho'l tumani", 'Paxtakor tumani', 'Yangiobod tumani', 'Zomin tumani', 'Zafarobod tumani', 'Zarbdar tumani', ], 'ru': 'Джизак', 'district_ru': ['Арнасойский район', 'Бархатный район', 'Район Дружбы', 'Форишский район', 'Галлаорольский район', 'Джизакский район', 'Мирзачельский район', 'Пахтакорский район', 'Янгиабадский район', 'Зоминский район', 'Зафарабадский район', 'Зарбдарский район', ]}, {'uz': 'Sirdaryo', 'district_uz': ['Akaltin tumani', 'Bayaut tumani', 'Guliston tumani', 'Xovast tumani', 'Mirzaobod tumani', 'Sayxunobod tumani', 'Sardoba tumani', 'Sirdaryo tumani', ], 'ru': 'Сырдарья', 'district_ru': ['Акалтинский район', 'Баяутский район', 'Гулистанский район', 'Ховастский район', 'Мирзаабадский район', 'Сайхунабадский район', 'Сардобинский район', 'Сырдарьинский район', ]}, {'uz': 'Toshkent', 'district_uz': ['Toshent shahri', 'Bekobod tumani', "Bo'stonliq tumani", 'Buka tumani', 'Chinoz tumani', 'Qibray tumani', 'Ohangaron tumani', "Oqqo'rg'on tumani", 'Parkent tumani', 'Piskent tumani', 'Quyi Chirchiq tumani', "O'rta Chirchiq tumani", "Yangiyo'l tumani", 'Yuqori Chirchiq tumani', 'Zangiata tumani', ], 'ru': 'Ташкент', 'district_ru': ['город Тошент.', 'Бекабадский район', 'Бостанлыкский район', 'Букинский район', 'Чинозский район', 'Кибрайский район', 'Охангаронский район', 'Аккурганский район', 'Паркентский район', 'Пискентский район', 'Нижний Чирчикский район', 'Средний Чирчикский район', 'Янгиельский район', 'Верхне-Чирчикский район', 'Зангиатинский район', ]}, {'uz': 'Namangan', 'district_uz': ['Chortoq tumani', 'Chust tumani', 'Kosonsoy tumani', 'Mingbuloq tumani', 'Namangan tumani', 'Norin tumani', 'Pap tumani', "To'raqo'rg'on tumani", "Uchqo'rg'on tumani", 'Uychi tumani', "Yangiqo'rg'on tumani", ], 'ru': 'Наманган', 'district_ru': ['Чортокский район', 'Чустский район', 'Косонсойский район', 'Мингбулокский район', 'Наманганский район', 'Норинский район', 'Папский район', 'Торакурганский район', 'Учкурганский район', 'Уйчинский район', 'Янгикурганский район', ]}, {'uz': "Farg'ona", 'district_uz': ['Oltiariq tumani', "Bag'dod tumani", 'Beshariq tumani', 'Buvayda tumani', "Dang'ara tumani", "Farg'ona tumani", 'Furqat tumani', "Qo'shtepa tumani", 'Quva tumani', 'Rishton tumani', "So'x tumani", 'Toshloq tumani', 'Uchko‘prik tumani', "O'zbekiston tumani", 'Yozyovon tumani', ], 'ru': 'Фергана', 'district_ru': ['Алтыарыкский район', 'Багдадский район', 'Бешарикский район', 'Бувайдский район', 'Дангаринский район', 'Ферганский район', 'Фуркатский район', 'Коштепинский район', 'Кувинский район', 'Риштанский район', 'Сохский район', 'Тошлокский район', 'Учкоприкский район', 'Район Узбекистана', 'Ёжиовонский район', ]}, {'uz': 'Andijon', 'district_uz': ['Andijon tumani', 'Asaka tumani', 'Baliqchi tumani', 'Boz tumani', 'Buloqboshi tumani', 'Izboskan tumani', 'Jalolquduq tumani', "Xo'jaobod tumani", 'Kurgontepa tumani', 'Marhamat tumani', "Oltinko'l tumani", 'Paxtaobod tumani', 'Shahrixon tumani', 'Ulugnor tumani', ], 'ru': 'Андижан', 'district_ru': ['Андижанский район', 'Асакинский район', 'Рыбацкий район', 'Бозский район', 'Булагбошинский район', 'Избосканский район', 'Жалалкудукский район', 'Ходжаабадский район', 'Кургонтепинский район', 'Мерхамат район', 'Олтынкольский район', 'Пахтаабадский район', 'Шахриханский район', 'Улугнорский район', ]}]
    for i in data:
        region = Regions.objects.create(uz_data=i["uz"],ru_data=i["ru"])
        for j,k in zip(i["district_uz"],i["district_ru"]):
            District.objects.create(region=region,uz_data=j,ru_data=k)
    return HttpResponse("Done")

@login_required_decorator
def write_diller(request):
    data = "Qoraqalpoq#Bahtiyor Nukus#94 143 00 00#Nukus tumani\nXorazm#Ilhom Xiva#90 077 74 77#Xiva tumani\nNavoiy#Akbar Navoiy#90 647 15 60#Navoiy tumani\nBuxoro#Jaloliddin Buxoro#91 924 40 04#Buxoro tumani\nSamarqand#Bexruz Samarqand#91 522 22 24#Samarqand tumani\nSamarqand#Sodiq Urgut#98 140 62 62#Urgut tumani\nSamarqand#Otabek-Bunyod Urgut#97 914 00 07#Urgut tumani\nQashqadaryo#Sherdor Kitob#97 388 70 31#Kitob tumani\nQashqadaryo#Asilbek Qarshi#99 555 51 55#Qarshi tumani\nSurxondaryo#Mansur Surxondaryo#97 898 00 40#Surxondaryo tumani\nJizzax#Dilshod Jizzax#91 942 91 98#Jizzax tumani\nToshkent#Umid Toshkent#98 300 71 27#Toshkent tumani\nNamangan#Abdurahmon Namangan#99 976 12 30#Abdurahmon tumani\nFarg'ona#Abduvoxid Texnogrand#97 663 11 10#Farg'ona tumani\nFarg'ona#lhom Qo'qon#91 151 82 52#Qo'qon tumani\nAndijon#Ulug'bek hoji Andijon#97 992 00 05#Andijon	"
    for i in data.split("\n"):
        a = i.split("#")
        # try:
        Diller.objects.create(status=1,name=a[1],number=a[2])
        # except:...
    return HttpResponse("Done")

def blabl(request):
    data = [{'name': 'start', 'uz_data': 'Давайте для начала выберем язык обслуживания! \r\nKeling, avvaliga xizmat ko’rsatish tilini tanlab olaylik.', 'ru_data': 'Давайте для начала выберем язык обслуживания!\r\nKeling, avvaliga xizmat ko’rsatish tilini tanlab olaylik.'}, {'name': 'request_name', 'uz_data': 'Ismingizni kiriting', 'ru_data': 'Введите ваше имя'}, {'name': 'request_number', 'uz_data': 'Telefon raqamingizni yuboring', 'ru_data': 'Отправьте свой номер телефона'}, {'name': 'send_number', 'uz_data': 'Yuborish 📞', 'ru_data': 'Отправить 📞'}, {'name': 'select_region', 'uz_data': 'Viloyatingizni tanlang 🏡', 'ru_data': 'Выберите свой область 🏡'}, {'name': 'select_district', 'uz_data': 'Tumaningizni tanlang 🏘', 'ru_data': 'Выберите свой район 🏘'}, {'name': 'district_not_found', 'uz_data': 'Afsuski bunday Tuman topilmadi  😕', 'ru_data': 'К сожалению, такой Район не найден  😕'}, {'name': 'region_not_found', 'uz_data': 'Afsuski, bunday viloyat topilmadi.😕', 'ru_data': 'К сожалению, такой регион не найден.😕'}, {'name': 'language_not_found', 'uz_data': 'Afsuski, bunday til topilmadi.😕', 'ru_data': 'К сожалению, такого языка не нашлось. 😕'}, {'name': 'order_accepted', 'uz_data': 'Buyurtmangiz qabul qilindi 🎉', 'ru_data': 'Ваш заказ принят 🎉'}, {'name': 'order_delivered', 'uz_data': "Buyurtmangiz tayyorlanib yo'lga chiqarildi 🚚", 'ru_data': 'Ваш заказ подготовлен и отправлен 🚚'}, {'name': 'order_denied', 'uz_data': "Buyurtmangiz ba'zi bir sabablarga ko'ra qabul qilinmadi. Qayta urinib ko'ring", 'ru_data': 'Ваш заказ не принят по какой-то причине. Попробуй снова'}, {'name': 'accept_message', 'uz_data': "Siz qabul qilindingiz. Boshlash uchun /start bu'yrug'ini yuboring", 'ru_data': 'Вы были приняты. Отправьте команду /start , чтобы начать'}, {'name': 'reject_message', 'uz_data': 'Siz qabul qilinmadingiz', 'ru_data': 'Вас не приняли'}, {'name': 'i_bought', 'uz_data': 'Sotib olingan', 'ru_data': 'Купленные'}, {'name': 'prompt_end', 'uz_data': 'Afsuski Aksiyamiz tugadi', 'ru_data': 'К сожалению, наша акция завершена.'}, {'name': 'promotion_count_message', 'uz_data': 'promotion_count_message', 'ru_data': 'promotion_count_message'}, {'name': 'promotion_count_error', 'uz_data': 'promotion_count_error', 'ru_data': 'promotion_count_error'}, {'name': 'empty_busket', 'uz_data': "Savat bo'sh 🛒", 'ru_data': 'Корзина пуста 🛒'}, {'name': 'pay_type', 'uz_data': "To'lov turini tanlang", 'ru_data': 'Выберите тип оплаты'}, {'name': 'cash', 'uz_data': 'Variant 1', 'ru_data': 'вариант 1'}, {'name': 'loan', 'uz_data': 'Variant 2', 'ru_data': 'вариант 2'}, {'name': 'no_orders', 'uz_data': 'Buyurtmalar mavjud emas', 'ru_data': 'Заказы недоступны'}, {'name': 'are_you_sure_get_gift', 'uz_data': "Ushbu sovg'ani qabul qilasizmi? 🎁", 'ru_data': 'Ты примешь этот подарок? 🎁'}, {'name': 'yes', 'uz_data': 'Ha', 'ru_data': 'да'}, {'name': 'no', 'uz_data': "Yo'q", 'ru_data': 'Нет'}, {'name': 'not_enought_balls', 'uz_data': 'Sizning ballingiz yetarli emas', 'ru_data': 'Твоего балла недостаточно'}, {'name': 'accept_your_prompt', 'uz_data': 'Aksiyamizda ishtirok etkanigniz uchun raxmat. Sizning buyurtmangiz adminlar tomonidan tasdiqlanib sizga javobini aytishadi', 'ru_data': 'Спасибо за участие в нашей кампании. Ваш заказ подтвердят администраторы и вам сообщат ответ'}, {'name': 'not_access', 'uz_data': 'Kechirasiz sizga hali ruhsat berilmagan .Iltimos kuting!', 'ru_data': 'Извините, вы еще не допущены. Пожалуйста, подождите!'}, {'name': 'taken', 'uz_data': 'Sotib olingan', 'ru_data': 'Купленные'}, {'name': 'buy', 'uz_data': 'Sotib olish', 'ru_data': 'Купить'}, {'name': 'my_balls', 'uz_data': 'Mening ballarim', 'ru_data': 'Мои баллы'}, {'name': 'send_cvitation', 'uz_data': 'Kvitansiyani rasimga olib yuboring', 'ru_data': 'Отправить квитанцию \u200b\u200b\u200b\u200bк картинке'}, {'name': 'send_cvi_serial_number', 'uz_data': 'Mahsulotning seria nomerini yuboring', 'ru_data': 'Отправьте серийный номер продукта'}, {'name': 'cvitation_success', 'uz_data': 'Muvoffaqiyatli amalga oshirildi. Mahsulot sotilganligi haqida dillerga habar yuborildi', 'ru_data': 'Успешно реализовано. Диллер был уведомлен о том, что товар продан.'}, {'name': 'already_sold', 'uz_data': 'Bu mahsulot allaqachon sotilgan', 'ru_data': 'Этот товар уже продан'}, {'name': 'seria_not_found', 'uz_data': 'Seria nomer topilmadi', 'ru_data': 'Серийный номер не найден'}, {'name': 'shop_name', 'uz_data': "Do'kon yoki firma nomini kiriting", 'ru_data': 'Введите название магазина или фирма'}, {'name': 'add_to_cart', 'uz_data': "🛒 Qo'shish", 'ru_data': '🛒 Добавить'}, {'name': 'order_btn', 'uz_data': 'Buyurtma berish ➡️', 'ru_data': 'Заказ ➡️'}, {'name': 'add_again_btn', 'uz_data': "➕yana qo'shish", 'ru_data': '➕Добавить больше'}, {'name': 'back_btn', 'uz_data': '⬅️ Ortga', 'ru_data': '⬅️ Назад'}, {'name': 'balls', 'uz_data': 'ball', 'ru_data': 'балл'}, {'name': 'diller_accept_order', 'uz_data': 'Qabul qildim ✔️', 'ru_data': 'Я принял ✔️'}, {'name': 'cvitation', 'uz_data': 'Kvitansiya', 'ru_data': 'Квитанция'}, {'name': 'menu', 'uz_data': 'Menu', 'ru_data': 'Меню'}, {'name': 'wait_accept', 'uz_data': "Ro'yhatdan o'tganingiz uchun raxmat.Sizga tez orada foydalanish uchun ruxsat beriladi", 'ru_data': 'Благодарим вас за регистрацию. Вскоре вам будет разрешено использовать его.'}, {'name': 'shop_location', 'uz_data': 'Lakatsiya yuboring', 'ru_data': 'Lakatsiya yuboring'}, {'name': 'shop_passport_photo', 'uz_data': 'Firma guvohnomasini yuboring', 'ru_data': 'Firma guvohnomasini yuboring'}, {'name': 'passport_photo', 'uz_data': 'Pasportingizni rasmini yuboring', 'ru_data': 'Pasportingizni rasmini yuboring'}, {'name': 'sum', 'uz_data': "so'm", 'ru_data': 'сум'}, {'name': 'price', 'uz_data': 'Narx', 'ru_data': 'Цена'}, {'name': 'product_count_limit', 'uz_data': 'product_count_limit', 'ru_data': 'product_count_limit'}, {'name': 'invalid_name', 'uz_data': 'Iltimos, toʻliq ismingizni kiriting!\r\nMisol uchun:\r\nKomiljonov Shukurullox', 'ru_data': 'Пожалуйста введите свое полное имя!\r\nтак:\r\nКомильжонов Шукуруллох'}, {'name': 'invalid_number', 'uz_data': "Telefon raqamini tog'ri yuboring", 'ru_data': "Telefon raqamini tog'ri yuboring"}, {'name': 'incorrect_shop_location', 'uz_data': "Lakatsiyani to'g'ri yuboring", 'ru_data': "Lakatsiyani to'g'ri yuboring"}, {'name': 'request_location', 'uz_data': 'Yuborish', 'ru_data': 'Отправить'}, {'name': 'you_are_deleted', 'uz_data': 'siz noto`gri ma`lumot kiritganligingiz sababli ushbu bordan chiqarildingiz', 'ru_data': 'siz noto`gri ma`lumot kiritganligingiz sababli ushbu bordan chiqarildingiz'}, {'name': 'total', 'uz_data': 'Umumiy summa', 'ru_data': 'Общая сумма'}, {'name': 'reject_check_text', 'uz_data': 'sizning {serial} seriali kvitansiyangiz qabul qiilinmadi hamda sizdan {ball} ball minus qilindi', 'ru_data': 'ваша серийная квитанция {serial} не была принята, и вы потеряли {ball}'}]

    for i in data:
        Text.objects.create(**i)
    return HttpResponse("Done")