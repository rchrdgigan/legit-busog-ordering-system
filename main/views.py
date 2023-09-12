from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users

from .models import PersonInfo, ProductInfo
from .forms import ProductInfoForm

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
            if user.groups.filter(name='Admin'):
                return redirect('admin.index')
            else:
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

        #For role
        group = Group.objects.get(name='Customer')
        user.groups.add(group)

        #personal information
        user = info.id
        perinfo = PersonInfo.objects.create(
            user=user, dob=dob, address=address, contact=contact)
        perinfo.save()

        messages.success(
            response, 'Your account has been successfully created')
        return redirect('login')

    return render(response, 'main/login_register/register.html')


@login_required
@allowed_users(allowed_roles=['Admin'])
def adminIndex(response):
    return render(response, 'main/admin/index.html')  # Admin

@login_required
@allowed_users(allowed_roles=['Admin'])
def adminCatList(response):
    dish_count = ProductInfo.objects.filter(category='Dish').count()
    dessert_count = ProductInfo.objects.filter(category='Dessert').count()
    drinks_count = ProductInfo.objects.filter(category='Drinks').count()
    return render(response, 'main/admin/categorylist.html', {
        'dish_count':dish_count,
        'dessert_count':dessert_count,
        'drinks_count':drinks_count,
    })  # Admin


@login_required
@allowed_users(allowed_roles=['Admin'])
def adminFoodList_Dish(response):
    food = ProductInfo.objects.filter(category='Dish')
    return render(response, 'main/admin/foodlist.html', {
        'food':food
    })  # Admin


@login_required
@allowed_users(allowed_roles=['Admin'])
def adminFoodList_Drinks(response):
    food = ProductInfo.objects.filter(category='Drinks')
    return render(response, 'main/admin/foodlist.html', {
        'food':food
    })  # Admin


@login_required
@allowed_users(allowed_roles=['Admin'])
def adminFoodList_Dessert(response):
    food = ProductInfo.objects.filter(category='Dessert')
    return render(response, 'main/admin/foodlist.html', {
        'food':food
    })  # Admin

@login_required
@allowed_users(allowed_roles=['Admin'])
def adminFoodCreate(response):
    
    if response.method == "POST":
        form = ProductInfoForm(response.POST, response.FILES)
        if form.is_valid():
            save = form.save(commit=False)
            save.user = response.user
            save.name = response.POST['food']
            save.category = response.POST['cat_id']
            save.price = response.POST['price']
            save.PrepTime = response.POST['ept']
            save.save()
            return redirect('admin_cat_list')
    form = ProductInfoForm()
    return render(response, 'main/admin/foodcreate.html', {
        'form':form
    })  # Admin


@login_required
@allowed_users(allowed_roles=['Admin'])
def adminFoodEdit(response, id):
    food = get_object_or_404(ProductInfo, id=id)
    form = ProductInfoForm(response.POST, response.FILES, instance=food)
    if response.method == "POST":
        form = ProductInfoForm(response.POST, response.FILES, instance=food)
        if form.is_valid():
            save = form.save(commit=False)
            save.name = response.POST['food']
            save.category = response.POST['cat_id']
            save.price = response.POST['price']
            save.PrepTime = response.POST['ept']
            save.save()
            return redirect('admin_cat_list')
    
    return render(response, 'main/admin/foodedit.html', {
        'form':form,
        'food':food,
    })


@login_required
@allowed_users(allowed_roles=['Admin'])
def adminFoodDelete(response, id):
    food = ProductInfo.objects.filter(id=id).first()
    food = get_object_or_404(ProductInfo, id=id)
    food.delete()
    return redirect('admin_cat_list')

def customerIndex(response):
    return render(response, 'main/customer/index.html')  # Customer
