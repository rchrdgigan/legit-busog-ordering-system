from django.shortcuts import render

# string path for admin and customer
strc = 'main/customer'
stra = 'main/admin'


def index(response):
    return render(response, 'main/home.html')
