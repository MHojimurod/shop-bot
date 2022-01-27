from django.shortcuts import render,redirect
from admin_panel.models import Regions,District
from diller.models import Diller
from myapp.models import Seller
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

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
def home(request):
    return render(request, "dashboard/index.html")


def dillers_list(request):
    dillers = Diller.objects.all()
    ctx = {
        "dillers": dillers,
        "d_active":"menu-open"
    }
    return render(request, "dashboard/dillers/list.html",ctx)



@login_required_decorator
def diller_update(request, pk,status):
    model = Diller.objects.get(pk=pk)
    model.delete()
    return redirect("dillers")


@login_required_decorator
def diller_delete(request, pk):
    model = Diller.objects.get(pk=pk)
    model.delete()
    return redirect("dillers")
