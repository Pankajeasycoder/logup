from django.shortcuts import render,redirect 
from django.contrib.auth import authenticate, login,logout
from .models import *
from .task import *
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
import random
def home(request):
    return render (request,"home.html")

def index(request):
    return render(request,"index.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password1")
        try:
            user=User.objects.get(username1=username)
        except:
            try:
                user=User.objects.get(email=username)
            except:
                user=None
        if user is not None:
            if user.check_password(password):
                if user.is_verified:
                    login(request,user)
                    if not(user.is_dealer or user.is_client):
                        return redirect()
            print("------------------------------")
            login(request, user)
            return redirect('index')  # Redirect to the 'home' URL
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
        email = request.POST['email']
        username=request.POST['username']
        password = request.POST['password']
        type=request.POST['redio']
        password_confirm = request.POST['password_confirm']

        if password == password_confirm:
                if User.objects.filter(username1=username).exists() or User.objects.filter(email=email).exists():
                    error_message=''
                    email_error=('',"Email is taken.")[User.objects.filter(email=email).exists():]
                    username_error=('',"Username is taken")[User.objects.filter(uaername1=username).exists():]
                    error_message=email_error + username_error
                    messages.success(request,error_message)
                    return redirect ("register")
                else:
                    if type =='client':
                        user=User.objects.create_user(email=email, username1=username, password=password)
                        user.is_client = True
                        user.save()
                        otp=random.randint(100000, 999999)
                        otpmodel=OTPModel(user=user, otp=otp)
                        otpmodel.save()
                        send_otp_with_celery.delay(email,otp)
                        subject= "OTP Verification From New_Gen"
                        message= f"Your OTP for Account Verification in New_Gen is {otp}"
                        send_mail(subject, message, 'b9c043482eca45', [email], fail_silently=False)
                        return redirect ("verify")
                    elif type =='dealer':

                        user = User.objects.create_user(email = email, username1 =username, password = password)
                        user.is_dealer = True
                        user.save()
                        otp = random.randint(100000, 999999)
                        otpmodel = OTPModel(user=user, otp=otp)
                        otpmodel.save()
                        send_otp_with_celery.delay(email,otp)
                        subject = "OTP Verification From New_gen"
                        message = f"Your OTP for Account Verification in New_Gen is {otp}"
                        send_mail(subject, message, 'b9c043482eca45', [email], fail_silently=False)
                        return redirect('verify')
                    else:
                        pass
                    return redirect ('register')
            
            
        else:
            messages.info(request, "password doesn't not match")
            return render(request, 'register.html')


    return render(request,"register.html")
# verify the user 
def verify(request):
    if request.method=='POST':
        otp=request.POST==['otp']
        otpuser=OTPModel.objects.filter(otp=otp).first()
        if otpuser is not None:
            user=User.objects.get(pk.otpuser.user.id)
            user.is_verified=True
            user.save()
            user.delete()
            login(request, user)
            if user.is_dealer:
                return redirect("login")
            elif user.is_client:
                return redirect ("login")
        else:
            messages.error(request,'OTP is incorrect.')
            return render (request,"verify.html")
    return render(request,"verify.html")
# profile according to user


def Dearler_Profile(request):

    return render (request,"dealerhome.html")


def Client_profile(request):

    return render (request,"clienthome.html")
# profile type 
def profile_type(request):
    if request.method=="POST":
        profiletype=request.POST['profiletype']
        login_user_id = request.user.id
        user= User.objects.get(pk=login_user_id)
        if profiletype == 'client':
            return redirect ('client')
        elif profiletype == 'dealer':
            return redirect ('dealer')
        else:
            return render(request,"profile.html", {'message': 'something went wrong please try again'})
    return render(request,"profile.html")

