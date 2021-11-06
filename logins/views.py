from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.translation import to_language
from .models import Temp_User
import random
from hashlib import sha256
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def index(request):
    return render(request, 'logins/index.html')

def login_view(request):
    if request.method=='POST':
        # username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
    return render(request, 'logins/login.html')

def signup_view(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        otp=otpGen()
        token=tokenGen()
        try:
            user=User.objects.get(email=email)
            if user is not None:
                messages.error(request, 'Email Already Registered')
                return redirect('/signup')
            tempuser=Temp_User.objects.create(username=username, email=email, password=password, otp=otp, token=token).save()
            send_varification_mail(otp, username, email)
            return render(request, 'logins/varify.html', {'token':token})
        except Exception as E:
            pass
    return render(request, 'logins/signup.html')


@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return redirect('/')

def otpGen():
    return random.randint(100000, 999999)

def tokenGen():
    token=str(random.random())
    token_hash=sha256(token.encode('utf-8')).hexdigest()
    return token_hash

def varify(request):
    if request.method=="POST":
        token=request.POST.get('token')
        otp=int(request.POST.get('otp'))
        try:
            temp_user=Temp_User.objects.get(token=token)
            if temp_user.otp==otp:
                username=temp_user.username
                email=temp_user.email
                password=temp_user.password
                print(password)
                user=User.objects.create(username=username, email=email)
                user.set_password(password)
                user.save()
                temp_user.delete()
                return redirect('/login')
            return render(request, 'logins/varify.html', {'token':token})
        except Exception as e:
            # user not found in temp user
            return redirect('/signup')
    return HttpResponse("<h1 style='text-align:center'>Not Found</h1>")

def send_varification_mail(otp, user, email):
    send_mail("Varification Mail", f'Hello {user},\nYour OTP for email varification on djreact is {otp}.\nThanks for signup', settings.EMAIL_HOST_USER, [email])

def forgot_password(request):
    if request.method=="POST":
        email=request.POST.get('email')
        otp=otpGen()
        token=tokenGen()
        # try:
        user=User.objects.get(email=email)
        if user is not None:
            temp_user=Temp_User.objects.create(email=email, otp=otp, token=token)
            return render(request, 'logins/login-with-otp.html', {'token':token})
        return redirect('/')
        # except Exception as E:
        return redirect('/')
    return render(request, 'logins/forgotpass.html')

def loginWithOTP(request):
    if request.method=="POST":
        token=request.POST.get("token")
        otp=int(request.POST.get('otp'))
        try:
            temp_user=Temp_User.objects.get(token=token)
            if otp==temp_user.otp:
                user=User.objects.get(email=temp_user.email)
                login(request, user)
                temp_user.delete()
                return redirect('/')
            return render(request, 'logins/login-with-otp.html', {'token':token})
        except Exception as E:
            return redirect('/login')

@login_required(login_url='/login')
def chpass(request):
    if request.method=="POST":
        old_pass=request.POST.get("pass_now")
        new_pass=request.POST.get("new_pass")
        email=request.user.email
        user=authenticate(email=email, password=old_pass)
        if user is not None:
            user=User.objects.get(email=email)
            user.set_password(new_pass)
            user.save()
            login(request, user)
            messages.success(request, 'Password changed successfully')
            return redirect('/')
        messages.success(request, 'Invalid Password')
        return redirect('/')
    return redirect('/')
