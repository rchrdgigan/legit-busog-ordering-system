from django.shortcuts import render

# string path for admin and customer
strc = 'main/customer'
stra = 'main/admin'


def index(response):
    return render(response, 'main/home.html')


def login(response):
    return render(response, 'main/login_register/login.html')


def register(response):
    return render(response, 'main/login_register/register.html')
