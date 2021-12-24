from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.contrib import auth
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .models import User

def login_reg(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('profile')
        
        login_form = LoginForm()
        register_form = RegisterForm()
        ctx = {
            "login": login_form,
            "reg": register_form,
        }
        return render(
            request,
            'index.html',
            context=ctx,
            status=200
        )

    if request.method == "POST":
        data = request.POST
        user = auth.authenticate(
            request,
            username=data["username"],
            password=data["password"]
        )
        
        if user is not None:
            auth.login(request, user)
            return redirect('profile')
        else:
            return redirect('login')
    
        
def registration(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        data = request.POST
        if data["password"] == data["passwprd2"]:
            user: User = User.objects.create_user(
                username=data["username"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                password=data["password"],
                bio=data["bio"],
                gender=data["gender"]
            )
            user.save()
            return redirect('login')

@login_required(login_url='login')
def profile(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        user: User = User.objects.filter(id=request.user.id).first()
        ctx = {
            "data": user
        }
        return render(
            request,
            "profile.html",
            context=ctx,
            status=200
        )
        
@login_required(login_url='login')
def search_result(request: HttpRequest) -> HttpResponse:
    
    if request.method == "GET":
        search_param = request.GET["search"]
        query = (
            Q(first_name__icontains=search_param) |
            Q(username__icontains=search_param)
        )
        users: User.objects = User.objects.filter(query)
        if users.exists():
            users = users.all()
        else:
            users = None
        ctx = {
            "data": users
        }
        print(users)
        return render(
            request,
            "search_result.html",
            context=ctx
        )

def logout(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('login')