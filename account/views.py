from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from account.models import Product


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products':products})

def about(request):
    return render(request, 'about.html')


def register(request):
    form = RegistrationForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            password1 = form.cleaned_data["password2"]

            if password1 == password:
                user.set_password(password1)
                user.customer = True
                user.save()
                return redirect("home")

        
    form = RegistrationForm()


    
    return render(request, 'account/register.html', {'form1':form})

def user_login(request):

    message = ''
    print(request)
    if request.method=="POST":
        form = LoginForm (request.POST)
        if form.is_valid():
            user=authenticate (
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )
            if user is not None:
                login(request,user)
                message = ("Logged successfully")
                return redirect("home")
            else:
                message = ("Login Failed ")
        else:
            message = form.errors

    form = LoginForm()
    return render(request, 'account/login.html', {'form1':form, 'message': message})

def user_logout(request):
    logout(request)
    return redirect("login")

# Create your views here