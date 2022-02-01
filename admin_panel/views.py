from django.shortcuts import render,redirect
from admin_panel.forms import CategoryForm, ProductForm
from admin_panel.models import Regions,District,Category,Product
from diller.models import Diller
from seller.models import Seller
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
        "d_active":"menu-open"
    }
    return render(request, "dashboard/diller.html",ctx)
 
@login_required_decorator   
def sellers_list(request):
    sellers = Seller.objects.order_by('-id').all()
    ctx = {
        "sellers": sellers,
        "s_active":"menu-open"
    }
    return render(request, "dashboard/seller.html",ctx)



@login_required_decorator
def diller_update(request, pk,status):
    Diller.objects.filter(pk=pk).update(status=status)
    data = requests.get(f"http://127.0.0.1:6002/diller_status", json={"data": {
            "id": pk,
            "status": status
        }})
    print(data.status_code)
    return redirect("home")


@login_required_decorator
def diller_delete(request, pk):
    model = Diller.objects.get(pk=pk)
    model.delete()
    return redirect("home")


@login_required_decorator
def seller_delete(request, pk):
    model = Seller.objects.get(pk=pk)
    model.delete()
    return redirect("sellers_list")

def checks(request):
    return render(request,"dashboard/checks.html")


def categories(request):
    category = Category.objects.all()
    
    ctx = {
        "categories": category,
    }
    return render(request,"dashboard/category/list.html",ctx)
def category_create(request):
    model = Category()
    form = CategoryForm(request.POST, request.FILES, instance=model)
    if form.is_valid():
        form.save()
        return redirect("categories")

    ctx = {
        "form": form,
    }
    return render(request,"dashboard/category/form.html",ctx)

@login_required_decorator
def category_edit(request, pk):
    model = Category.objects.get(pk=pk)
    form = CategoryForm(request.POST or None, request.FILES or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect("categories")
        else:
            print(form.errors)
    ctx = {"form": form}
    return render(request, "dashboard/category/form.html", ctx)

def category_delete(request, pk):
    model = Category.objects.get(pk=pk)
    model.delete()
    return redirect("categories")




def products(request,category_id):
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category_id=category_id)
    ctx = {
        "products": products,
        "category": category,
    }
    return render(request,"dashboard/product/list.html",ctx)


def product_create(request,pk):
    model = Product()
    form = ProductForm(request.POST, request.FILES, instance=model)
    if form.is_valid():
        data = form.save()
        return redirect(f"/products/{data.category_id}")

    ctx = {
        "form": form,
        "pk":pk
    }
    return render(request,"dashboard/product/form.html",ctx)

@login_required_decorator
def product_edit(request, pk,category_id):
    model = Product.objects.get(pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=model)
    if request.POST:
        if form.is_valid():
            data = form.save()
            return redirect(f"/products/{data.category_id}")
        else:
            print(form.errors)
    ctx = {"form": form,
            "pk":category_id
        }
    return render(request, "dashboard/product/form.html", ctx)

def product_delete(request, pk):
    model = Product.objects.get(pk=pk)
    model.delete()
    return redirect(f"/products/{model.category_id}")