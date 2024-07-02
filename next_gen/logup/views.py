from django.shortcuts import render,redirect 
from django.contrib.auth import authenticate, login,logout
from .models import User
from django.contrib import messages

def home(request):
    return render (request,"home.html")

def index(request):
    return render(request,"index.html")

def login_page(request):
    if request.method == "POST":
        print("================")
        hello = request.POST.get("username")
        password = request.POST.get("password1")
        print(hello,"username--------")
        print(password,"password--------------")
        user = authenticate(email=hello, password=password)
        print(user,"user------------------------------")
        if user is not None:
            print("------------------------------")
            login(request, user)
            return redirect('home')  # Redirect to the 'home' URL
        else:
            print("else ====================")
            messages.error(request, "Please check your email/password")
            return render(request, "login.html")

    return render(request, "login.html")


def signout(request):
    logout(request)
    return redirect("home")

def register(request):
    if request.method == 'POST':
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password == password_confirm:
            email = request.POST['email']
            user = User.objects.create_user( email=email, password=password)
            user.is_member =True
            user.save()
            messages.info(request, "User Added Successfully")
            return redirect("login")
        
        else:
            messages.info(request, "password doesn't not match")
            return render(request, 'register.html')


    return render(request,"register.html")


