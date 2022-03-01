import pstats
from pyexpat import model
from django.shortcuts import render, redirect
from telegram import TelegramDecryptionError
from admin_panel.forms import CategoryForm, DistrictForm, GiftsForm, ProductForm, PromotionForm, RegionsForm, SoldForm, TextForm
from admin_panel.models import BaseProduct, Gifts, Promotion_Order, Regions, District, Category, Product, Text, Promotion
from diller.models import Diller, Busket, Busket_item, OrderGiftDiller
from seller.models import Cvitation, OrderGiftSeller, Seller
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import requests


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
def sellers_list(request):
    sellers = Seller.objects.order_by('-id').all()
    print(sellers)
    ctx = {
        "sellers": sellers,
        "sel_active": "menu-open"
    }
    return render(request, "dashboard/seller.html", ctx)


@login_required_decorator
def diller_update(request, pk, status):
    Diller.objects.filter(pk=pk).update(status=status)
    data = requests.get(f"http://127.0.0.1:6002/diller_status", json={"data": {
        "id": pk,
        "status": status
    }})
    return redirect("home")


@login_required_decorator
def diller_delete(request, pk):
    model = Diller.objects.get(pk=pk)
    model.delete()
    return redirect("home")


@login_required_decorator
def seller_delete(request, pk):
    model = Seller.objects.get(pk=pk)
    requests.get(f"http://127.0.0.1:6003/delete_seller", json={"data": {
        "id": pk,
    }})
    return redirect("sellers_list")


@login_required_decorator
def checks(request):
    cvitation = Cvitation.objects.order_by("-id").all()
    ctx = {
        "checks": cvitation,
        "ch_active":"menu-open"
    }
    return render(request, "dashboard/checks.html", ctx)


@login_required_decorator
def categories(request):
    category = Category.objects.all()

    ctx = {
        "categories": category,
        "cat_active":"menu-open"
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
        "r_active":"menu-open"
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
        "r_active":"menu-open"
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
    ctx = {"form": form,"r_active":"menu-open"}
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
        "r_active":"menu-open"
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
        "r_active":"menu-open"
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
           "r_active":"menu-open"
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
    busket = Busket.objects.filter(status__in=[0, 1],is_ordered=True)
    data = []
    for i in busket:
        diller = i.diller

        text = ""
        ball = 0
        for j in Busket_item.objects.filter(busket=i):
            text += f"{j.product.name_uz} x {j.count} = {j.product.price * j.count}<br>"
            ball += j.product.diller_ball*j.count

        data.append(
            {
                "diller": diller,
                "text": text,
                "ball": ball,
                "busket": i
            })
    ctx = {
        "items": data,
        "dil_active": "active"

    }

    return render(request, "dashboard/order/list.html", ctx)


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
    ctx = {
        "baseproduct": all,
        "s_active": "menu-open"
    }
    return render(request, "dashboard/sold/list.html", ctx)


@login_required_decorator
def sold_create(request):
    model = BaseProduct()
    form = SoldForm(request.POST, instance=model)
    if form.is_valid():
        form.save()
        return redirect("solds")

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
    # print(request.POST)
    if form.is_valid():
        print("aa")
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


def order_gift(request):
    diller: OrderGiftDiller = OrderGiftDiller.objects.all()
    seller: OrderGiftSeller = OrderGiftSeller.objects.all()

    ctx = {
        "diller": diller,
        "seller": seller,
        "gift_active": "active"
    }
    return render(request, "dashboard/gifts/order.html", ctx)


def update_gift(request, pk, status, type_order):
    if type_order == 0:
        OrderGiftDiller.objects.filter(pk=pk).update(status=status)
    elif type_order == 1:
        OrderGiftSeller.objects.filter(pk=pk).update(status=status)
    return redirect("order_gift")
