from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib import messages

from .models import PersonInfo

# string path for admin and customer
strc = 'main/customer'
stra = 'main/admin'


def index(response):
    return render(response, 'main/home.html')


def login(response):
    if response.method == "POST":
        username = response.POST['username']
        password = response.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            dj_login(response, user)
            return redirect('index')
        else:
            messages.error(response, "Invalid Credentials")

    return render(response, 'main/login_register/login.html')


def logout(response):
    dj_logout(response)
    return redirect('index')


def register(response):
    if response.method == "POST":
        first_name = response.POST['first_name']
        last_name = response.POST['last_name']
        dob = response.POST['date_of_birth']
        address = response.POST['address']
        contact = response.POST['contact']
        email = response.POST['email']
        password = response.POST['password']

        if User.objects.filter(username=email):
            messages.error(
                response, "Email already exist. Please try another email")
            return redirect('register')
        if len(password) < 8:
            messages.error(
                response, "Password must contain 8 or more character")
            return redirect('register')
        if not password.isalnum():
            messages.error(
                response, 'Password must contain Alpha-Numeric character')
            return redirect('register')

        info = User.objects.create_user(
            username=email, email=email, password=password)
        info.first_name = first_name
        info.last_name = last_name
        info.save()
        user = info.id
        perinfo = PersonInfo.objects.create(
            user=user, dob=dob, address=address, contact=contact)
        perinfo.save()
        messages.success(
            response, 'Your account has been successfully created')
        return redirect('login')

    return render(response, 'main/login_register/register.html')


def orderTracking(response):
    return render(response, 'main/order/index.html')
