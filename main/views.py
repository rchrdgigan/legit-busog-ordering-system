from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users

from .models import PersonInfo, ProductInfo, Category
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
    user = response.user
    dj_logout(response)
    if user.groups.filter(name='Admin'):
        return redirect('login')
    else:
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

        # For role
        group = Group.objects.get(name='Customer')
        user.groups.add(group)

        # Personal Information
        user = info.id
        perinfo = PersonInfo.objects.create(
            user=user, dob=dob, address=address, contact=contact)
        perinfo.save()
        messages.success(
            response, 'Your account has been successfully created')
        return redirect('login')

    return render(response, 'main/login_register/register.html')


@login_required
def changePassword(response):
    if response.method == "POST":
        user = response.user
        form = PasswordChangeForm(user=response.user, data=response.POST)
        if form.is_valid():
            form.save()
            dj_logout(response)
            if user.groups.filter(name='Admin'):
                return redirect('login')
            else:
                return redirect('index')
        else:
            messages.error(response, 'Invalid Input!')
            if user.groups.filter(name='Admin'):
                return redirect('admin.index')
            else:
                return redirect('index')

    else:
        form = PasswordChangeForm(user=response.user)
        return render(response, 'main/login_register/change_password.html', {
            'form': form,
        })

    # if new_pass != new_pass_confirm:
    #     messages.error(response, 'Error! Password Confirmation not match!')
    #     if user.groups.filter(name='Admin'):
    #         return redirect('admin.index')
    #     else:
    #         return redirect('index')
    # # elif len(new_pass) < 8 or len(new_pass_confirm) < 8:
    # #     messages.error(response, "Password must contain 8 or more character")
    # #     if user.groups.filter(name='Admin'):
    # #         return redirect('admin.index')
    # #     else:
    # #         return redirect('index')
    # elif not new_pass.isalnum() or not new_pass_confirm.isalnum():
    #     messages.error(response, 'Password must contain Alpha-Numeric character')
    #     if user.groups.filter(name='Admin'):
    #         return redirect('admin.index')
    #     else:
    #         return redirect('index')
    # else:
    #     user.set_password(new_pass)
    #     user.save()
    #     dj_logout(response)
    # return redirect('login')


@login_required
@allowed_users(allowed_roles=['Admin'])
def adminIndex(response):
    user = response.user
    return render(response, 'main/admin/index.html', {
        'user': user,
    })  # Admin


@login_required
@allowed_users(allowed_roles=['Admin'])
def adminCatList(request):
    cat = Category.objects.all()
    if request.method == "POST":
        user = request.user
        category = request.POST['cat']
        data = Category(user=user, category_name=category)
        data.save()
        messages.success(request, 'Category Has Been Added!')
        return redirect('admin_cat_list')
    category_product_counts = {}
    for category in cat:
        product_count = ProductInfo.objects.filter(
            category=category.category_name).count()
        category_product_counts[category.category_name] = product_count
    return render(request, 'main/admin/categorylist.html', {
        'cat': cat,
        'category_product_counts': category_product_counts,
    })  # Admin


@login_required
@allowed_users(allowed_roles=['Admin'])
def adminCatUpdate(request):
    if request.method == "POST":
        cat_id = request.POST.get('id')
        cat = Category.objects.get(id=cat_id)
        cat.category_name = request.POST['cat']
        cat.save()
        messages.success(request, 'Data successfully updated!')
        return redirect('admin_cat_list')
    else:
        messages.error(
            request, 'Form is not valid. Please check the data.')
    return HttpResponseBadRequest('Invalid request method')


@login_required
@allowed_users(allowed_roles=['Admin'])
def adminFoodCat(response, id):
    category = Category.objects.get(id=id)
    food = ProductInfo.objects.filter(category=category.category_name)
    return render(response, 'main/admin/foodlist.html', {
        'food': food,
        'category': category,
    })  # Admin


@login_required
@allowed_users(allowed_roles=['Admin'])
def adminFoodCreate(response, id):
    category = Category.objects.get(id=id)
    food = ProductInfo.objects.filter(category=category)
    if response.method == "POST":
        form = ProductInfoForm(response.POST, response.FILES)
        if form.is_valid():
            save = form.save(commit=False)
            save.user = response.user
            save.name = response.POST['food']
            save.price = response.POST['price']
            save.PrepTime = response.POST['ept']
            save.category = response.POST['cat_id']
            save.description = response.POST['description']
            save.save()
            messages.success(
                response, 'Your Product Has Been Successfully Added!')
            return redirect('admin_food_cat', category.id)
        else:
            HttpResponse('Invalid!')

    form = ProductInfoForm()
    cat_all = Category.objects.all()
    return render(response, 'main/admin/foodcreate.html', {
        'form': form,
        'food': food,
        'cat_all': cat_all

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
            save.description = response.POST['description']
            save.save()
            if save:
                messages.success(response, 'Data successfully updated!')
                return redirect('admin_cat_list')
    cat = Category.objects.all().exclude(category_name=food.category)
    return render(response, 'main/admin/foodedit.html', {
        'form': form,
        'food': food,
        'cat': cat,
    })


@login_required
@allowed_users(allowed_roles=['Admin'])
def adminViewFeedback(response):

    return render(response, 'main/admin/feedbacklist.html')  # Admin


@login_required
@allowed_users(allowed_roles=['Admin'])
def adminViewAccount(response):

    return render(response, 'main/admin/accountlist.html')  # Admin


@login_required
@allowed_users(allowed_roles=['Admin'])
def adminFoodDelete(response, id2, id):
    cat = Category.objects.filter(id=id2).first()
    food = ProductInfo.objects.filter(category=cat, id=id)
    food = get_object_or_404(ProductInfo, id=id)
    food.delete()
    messages.error(response, 'Product Has Been Deleted!')
    return redirect('admin_food_cat', cat.id)


@login_required
@allowed_users(allowed_roles=['Admin'])
def adminFoodAvailable(response, ida, id):
    print(1)
    cat = Category.objects.filter(id=ida).first()
    food = ProductInfo.objects.filter(category=cat, id=id)
    food = get_object_or_404(ProductInfo, id=id)
    data = ProductInfo.objects.get(name=food.name, category=food.category, price=food.price,
                                   PrepTime=food.PrepTime, description=food.description, image=food.image)
    data.availability = True
    data.save()
    messages.success(response, 'Successfully Changed The Status!')
    return redirect('admin_food_cat', cat.id)


@login_required
@allowed_users(allowed_roles=['Admin'])
def adminFoodUnavailable(response, ida, id):
    print(2)
    cat = Category.objects.filter(id=ida).first()
    food = ProductInfo.objects.filter(category=cat, id=id)
    food = get_object_or_404(ProductInfo, id=id)
    data = ProductInfo.objects.get(name=food.name, category=food.category, price=food.price,
                                   PrepTime=food.PrepTime, description=food.description, image=food.image)
    data.availability = False
    data.save()
    messages.success(response, 'Successfully Changed The Status!')
    return redirect('admin_food_cat', cat.id)


def customerIndex(response):
    return render(response, 'main/customer/index.html')  # Customer
