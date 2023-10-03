from contextlib import nullcontext
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from datetime import date
from django.db.models import Q

from .models import ContactUs, FeedBack, Order, PersonInfo, ProductInfo, Category, Transaction
from .forms import ProductInfoForm

# string path for admin and customer
strc = 'main/customer'
stra = 'main/admin'


@login_required
def customerPlaceOrder(response):
    user = response.user
    if Order.objects.filter(user=user, status='In-Summary'):
        in_summ_order = Order.objects.filter(user=user, status='In-Summary')
        for in_summ in in_summ_order:
            datas = get_object_or_404(Order, id=in_summ.id)
            datas.status = 'In-Cart'
            datas.save()
    if Transaction.objects.filter(user=user, status='In-Summary'):
        in_summ_trans = Transaction.objects.get(user=user, status='In-Summary')
        in_summ_trans.status = 'In-Cart'
        in_summ_trans.save()

    if Order.objects.filter(user=user, status='In-Cart'):
        orders = Order.objects.filter(user=user, status='In-Cart')
        for order in orders:
            ords = Order.objects.get(id=order.id)
            break

        if Transaction.objects.filter(transaction_id=ords.transaction_id):
            transaction = get_object_or_404(
                Transaction, transaction_id=ords.transaction_id)
        else:
            transaction = Transaction(
                transaction_id=ords.transaction_id, user=user)
            transaction.save()
        transaction.total_amount = 0
        transaction.save()

        for order in orders:
            total_order = transaction.total_amount + order.total_amount
            transaction.total_amount = total_order
            transaction.save()

        if response.method == "POST":
            if response.POST.getlist('checkbox'):
                datalist = response.POST.getlist('checkbox')
                transaction.status = 'In-Summary'
                transaction.save()
                for data in datalist:
                    ords = get_object_or_404(Order, id=data)
                    ords.status = 'In-Summary'
                    ords.save()
                return redirect('customer_summary_order')
            else:
                messages.error(
                    response, "Please select the product you want to check out")
    else:
        orders = ''
        transaction = ''
    return render(response, 'main/pages/placeorder.html', {
        'orders': orders,
        # 'data': data,
        'transaction': transaction,
    })


def customerDeleteOneOrder(request, order_id):
    order = get_object_or_404(
        Order, id=order_id, user=request.user, status='In-Cart')
    order.delete()
    messages.error(request, 'Successfully removed from the cart!')
    return redirect('customer_placeorder_order')


def customerDeleteOneOrderSummary(response, id):
    order = get_object_or_404(Order, id=id)
    order.delete()
    messages.error(response, 'Successfully removed from the order summary!')
    return redirect('customer_summary_order')


def foodProductList(request):
    search_query = request.GET.get('search', '')
    foods = ProductInfo.objects.filter(
        Q(name__icontains=search_query) | Q(category__icontains=search_query)
    )
    return render(request, 'main/pages/foodproduct.html', {
        'foods': foods,
        'search_query': search_query,
    })


@login_required
def foodProductShow(response, id):
    food = ProductInfo.objects.get(id=id)
    user = response.user
    if response.method == "POST":
        if user.is_authenticated:
            quantity = response.POST['product-qty']
            if Order.objects.filter(user=user, status='In-Cart'):
                order_incart = Order.objects.filter(
                    user=user, status='In-Cart')
                for o in order_incart:
                    o = Order.objects.get(id=o.id)
                    break
                order = Order(user=user, product=food,
                              quantity=quantity)
                order.total_amount = int(quantity) * int(order.product.price)
                if Order.objects.filter(user=user, status='Single-Order'):
                    single_order = Order.objects.filter(
                        user=user, status='Single-Order')
                    for single in single_order:
                        singles = Order.objects.get(id=single.id)
                        singles.delete()
                if response.POST.get('addcart'):
                    if order_incart:
                        order.status = 'In-Cart'
                        order.transaction_id = o.transaction_id
                        order.save()
                    else:
                        order.save()
                    return redirect('main_food_added')
                else:
                    order.status = 'Single-Order'
                    order.save()
                    return redirect('customer_single_order')
            else:
                order = Order(user=user, product=food,
                              quantity=quantity)
                order.total_amount = int(quantity) * int(order.product.price)
                if Order.objects.filter(user=user, status='Single-Order'):
                    single_order = Order.objects.filter(
                        user=user, status='Single-Order')
                    for single in single_order:
                        singles = Order.objects.get(id=single.id)
                        singles.delete()
                if response.POST.get('addcart'):
                    order.status = 'In-Cart'
                    order.save()
                    return redirect('main_food_added')
                else:
                    order.status = 'Single-Order'
                    order.save()
                    return redirect('customer_single_order')
        else:
            return redirect('login')

    return render(response, 'main/pages/viewproduct.html', {
        'food': food,
    })


@login_required
def foodBuySucessfully(response):
    return render(response, 'main/pages/successfully-ordered.html')


def foodAdded(response):
    return render(response, 'main/pages/successfully-added.html')


def ViewProductByCategory(response, id):
    category = Category.objects.get(id=id)
    foods = ProductInfo.objects.filter(
        category=category.category_name, availability=True)
    return render(response, 'main/pages/viewproductbycategory.html', {
        'foods': foods,
        'category': category,
    })


def index(response):
    category = Category.objects.all()
    foods = ProductInfo.objects.all()
    if response.method == "POST":
        name = response.POST['name']
        email = response.POST['email']
        message = response.POST['message']
        save = ContactUs(user=response.user, name=name,
                         email=email, message=message)
        save.save()
        messages.success(response, 'Your inquiries has been submitted!')
    return render(response, 'main/home.html', {
        'category': category,
        'foods': foods,
    })


def login(response):
    if response.method == "POST":
        username = response.POST['username']
        password = response.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            dj_login(response, user)
            if user.groups.filter(name='admin'):
                return redirect('admin.index')
            else:
                return redirect('index')
        else:
            messages.error(response, "Invalid Credentials")

    return render(response, 'main/login_register/login.html')


def logout(response):
    user = response.user
    dj_logout(response)
    if user.groups.filter(name='admin'):
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
        group = Group.objects.get(name='customer')
        info.groups.add(group)

        # Personal Information
        user = info
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
            if user.groups.filter(name='admin'):
                return redirect('login')
            else:
                return redirect('index')
        else:
            messages.error(response, 'Invalid Input!')
            if user.groups.filter(name='admin'):
                return redirect('admin.index')
            else:
                return redirect('index')

    else:
        form = PasswordChangeForm(user=response.user)
        return render(response, 'main/login_register/change_password.html', {
            'form': form,
        })


@login_required
@allowed_users(allowed_roles=['admin'])
def adminIndex(response):
    user = response.user
    count_pending = Transaction.objects.filter(status='Pending').count()
    count_processing = Transaction.objects.filter(status='In-Process').count()
    count_deliver = Transaction.objects.filter(
        status='Out for Delivery').count()
    count_pd = count_processing + count_deliver
    count_completed = Transaction.objects.filter(status='Completed').count()
    orders = Order.objects.filter(status='Pending')
    trans = Transaction.objects.filter(status='Pending')
    return render(response, 'main/admin/index.html', {
        'user': user,
        'count_pending': count_pending,
        'count_processing': count_processing,
        'count_completed': count_completed,
        'count_pd': count_pd,
        'orders': orders,
        'trans': trans,
    })  # Admin


@login_required
@allowed_users(allowed_roles=['admin'])
def adminCatList(request):
    cat = Category.objects.all()
    if request.method == "POST":
        user = request.user
        category = request.POST['cat']
        image = request.FILES.get('image')
        data = Category(user=user, category_name=category, img=image)
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
@allowed_users(allowed_roles=['admin'])
def adminCatUpdate(request, id):
    cat = Category.objects.get(id=id)
    if request.method == "POST":
        cat.category_name = request.POST['cat']
        cat.img = request.FILES.get('image')
        cat.save()
        messages.success(request, 'Data successfully updated!')
        return redirect('admin_cat_list')
    else:
        messages.error(
            request, 'Form is not valid. Please check the data.')
    return HttpResponseBadRequest('Invalid request method')


@login_required
@allowed_users(allowed_roles=['admin'])
def adminFoodCat(response, id):
    category = Category.objects.get(id=id)
    food = ProductInfo.objects.filter(category=category.category_name)
    return render(response, 'main/admin/foodlist.html', {
        'food': food,
        'category': category,
    })  # Admin


@login_required
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
def adminViewFeedback(response):
    feedbacks = FeedBack.objects.all()
    return render(response, 'main/admin/feedbacklist.html', {
        'feedbacks': feedbacks,
    })  # Admin


@login_required
@allowed_users(allowed_roles=['admin'])
def adminDeleteFeeback(response, id):
    feedback = FeedBack.objects.get(id=id)
    feedback.delete()
    messages.error(response, 'Feedback has been deleted!')
    return redirect('admin_feedback_list')


@login_required
@allowed_users(allowed_roles=['admin'])
def adminViewAccount(response):
    group = Group.objects.get(name='customer')
    users = User.objects.filter(groups=group)
    return render(response, 'main/admin/accountlist.html', {
        'users': users
    })  # Admin


@login_required
@allowed_users(allowed_roles=['admin'])
def adminUserChangePass(response, id):
    user = User.objects.get(id=id)
    if response.method == "POST":
        form = SetPasswordForm(user=user, data=response.POST)
        if form.is_valid():
            form.save()
            messages.success(response, 'Successfully Changed The Password!')
            return redirect('admin_account_list')
        else:
            messages.error(response, 'Invalid Input!')
            return redirect('admin_account_list')
    else:
        form = SetPasswordForm(user=user)
        return render(response, 'main/login_register/customer_change_pass.html', {
            'form': form,
        })


@login_required
@allowed_users(allowed_roles=['admin'])
def adminFoodDelete(response, id2, id):
    cat = Category.objects.filter(id=id2).first()
    food = ProductInfo.objects.filter(category=cat, id=id)
    food = get_object_or_404(ProductInfo, id=id)
    food.delete()
    messages.error(response, 'Product Has Been Deleted!')
    return redirect('admin_food_cat', cat.id)


@login_required
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
def adminFoodUnavailable(response, ida, id):
    cat = Category.objects.filter(id=ida).first()
    food = ProductInfo.objects.filter(category=cat, id=id)
    food = get_object_or_404(ProductInfo, id=id)
    data = ProductInfo.objects.get(name=food.name, category=food.category, price=food.price,
                                   PrepTime=food.PrepTime, description=food.description, image=food.image)
    data.availability = False
    data.save()
    messages.success(response, 'Successfully Changed The Status!')
    return redirect('admin_food_cat', cat.id)


@login_required
@allowed_users(allowed_roles=['admin'])
def adminPendingOrder(response):
    trans = Transaction.objects.filter(status='Pending')
    return render(response, 'main/admin/orderpending.html', {
        'trans': trans,
    })  # admin


@login_required
@allowed_users(allowed_roles=['admin'])
# Confirm order move to in-process category
def adminToProcessOrder(response, id):
    transaction = Transaction.objects.get(id=id)
    transaction.status = 'In-Process'
    transaction.save()
    orders = Order.objects.filter(transaction_id=transaction.transaction_id)
    for order in orders:
        ords = Order.objects.get(id=order.id)
        ords.status = 'In-Process'
        ords.save()
    messages.success(
        response, 'Order has been confirmed! It will move now to In-Process...')
    return redirect('admin_pending_order')


@login_required
@allowed_users(allowed_roles=['admin'])
def adminProcessOrder(response):
    trans = Transaction.objects.filter(
        status='In-Process') | Transaction.objects.filter(status='Out for Delivery')
    return render(response, 'main/admin/orderinprocess.html', {
        'trans': trans,
    })  # admin


@login_required
@allowed_users(allowed_roles=['admin'])
def adminToDeliverOrder(response, id):
    transaction = Transaction.objects.get(id=id)
    transaction.status = 'Out for Delivery'
    transaction.save()
    orders = Order.objects.filter(transaction_id=transaction.transaction_id)
    for order in orders:
        ords = Order.objects.get(id=order.id)
        ords.status = 'Out for Delivery'
        ords.save()
    messages.success(response, 'Order is out for delivery!')
    return redirect('admin_process_order')


@login_required
@allowed_users(allowed_roles=['admin'])
# Confirm order move to completed category
def adminToCompleteOrder(response, id):
    transaction = Transaction.objects.get(id=id)
    transaction.status = 'Completed'
    transaction.save()
    orders = Order.objects.filter(transaction_id=transaction.transaction_id)
    for order in orders:
        ords = Order.objects.get(id=order.id)
        ords.status = 'Completed'
        ords.save()
    messages.success(response, 'Order has been completed!')
    return redirect('admin_process_order')


@login_required
@allowed_users(allowed_roles=['admin'])
def adminCompletedOrder(response):
    trans = Transaction.objects.filter(status='Completed')
    return render(response, 'main/admin/ordercompleted.html', {
        'trans': trans,
    })  # admin


@login_required
@allowed_users(allowed_roles=['admin'])
def adminCancellingOrder(response, id):
    trans = Transaction.objects.get(id=id)
    order = Order.objects.filter(transaction_id=trans.transaction_id)
    if response.method == "POST":
        reason = response.POST.get('reason')
        trans.status = 'Cancelled'
        trans.cancel_reason = reason
        trans.save()
        for ords in order:
            o = Order.objects.get(id=ords.id)
            o.status = 'Cancelled'
            o.save()
        messages.error(response, 'Order has been cancelled!')
        return redirect('admin_pending_order')
    else:
        return HttpResponse('invalid')


@login_required
@allowed_users(allowed_roles=['admin'])
def adminCancelledOrder(response):
    trans = Transaction.objects.filter(status='Cancelled')
    return render(response, 'main/admin/ordercancelled.html', {
        'trans': trans
    })  # admin


@login_required
@allowed_users(allowed_roles=['admin'])
def adminProfile(response):
    user = response.user
    try:
        person = PersonInfo.objects.get(user=user)
    except PersonInfo.DoesNotExist:
        person = None
    return render(response, 'main/admin/profile.html', {
        'user': user,
        'person': person,
    })  # admin


@login_required
@allowed_users(allowed_roles=['admin'])
def adminEditProfile(response, id):
    user = get_object_or_404(User, id=id)
    try:
        person = PersonInfo.objects.get(user=user)
    except PersonInfo.DoesNotExist:
        person = None
    if response.method == "POST":
        user.first_name = response.POST['fname']
        user.last_name = response.POST['lname']
        user.email = response.POST['email']
        user.save()
        if person:
            person.address = response.POST['address']
            person.dob = response.POST['dob']
            person.contact = response.POST['contact']
            person.save()
        else:
            PersonInfo.objects.create(
                user=user,
                address=response.POST['address'],
                dob=response.POST['dob'],
                contact=response.POST['contact']
            )
        messages.success(response, 'Successfully updated your profile!')
        return redirect('admin_profile')

    return render(response, 'main/admin/editprofile.html', {
        'user': user,
        'person': person,
    })  # admin


@login_required
@allowed_users(allowed_roles=['admin'])
def adminChangePicture(response, id):
    user = User.objects.get(id=id)
    try:
        person = PersonInfo.objects.get(user=user)
    except PersonInfo.DoesNotExist:
        person = None
    if response.method == "POST":
        person.image = response.FILES['image']
        person.save()
        messages.success(response, 'Successfully changed profile picture!')
        return redirect('admin_profile')
    return render(response, 'main/admin/changepicture.html', {
        'person': person,
    })  # admin


@login_required
@allowed_users(allowed_roles=['admin'])
def adminMessagesList(response):
    msg = ContactUs.objects.all()
    return render(response, 'main/admin/contactlist.html', {
        'msg': msg
    })


@login_required
@allowed_users(allowed_roles=['admin'])
def adminDeleteMessage(response, id):
    msg = ContactUs.objects.get(id=id)
    msg.delete()
    messages.success(response, 'Message has been deleted!')
    return redirect('admin_messages_list')


@login_required
@allowed_users(allowed_roles=['admin'])
def adminViewOrderListPending(response, trans_id):
    orders = Order.objects.filter(transaction_id=trans_id, status='Pending')
    return render(response, 'main/admin/viewitemlist.html', {
        'orders': orders,
        'trans': Transaction.objects.filter(transaction_id=trans_id),
        'total_amount': sum(order.total_amount for order in orders)
    })  # admin


@login_required
@allowed_users(allowed_roles=['admin'])
def adminViewOrderListInProcess(response, trans_id):
    trans = Transaction.objects.filter(transaction_id=trans_id)
    orders = Order.objects.filter(transaction_id=trans_id, status='In-Process') | Order.objects.filter(
        transaction_id=trans_id, status='Out for Delivery')
    return render(response, 'main/admin/viewitemlist.html', {
        'orders': orders,
        'trans': trans,
        'total_amount': sum(order.total_amount for order in orders)
    })  # admin


@login_required
@allowed_users(allowed_roles=['admin'])
def adminViewOrderListCompleted(response, trans_id):
    trans = Transaction.objects.filter(transaction_id=trans_id)
    orders = Order.objects.filter(transaction_id=trans_id, status='Completed')
    return render(response, 'main/admin/viewitemlist.html', {
        'orders': orders,
        'trans': trans,
        'total_amount': sum(order.total_amount for order in orders)
    })  # admin


@login_required
def customerIndex(response):
    user = response.user
    person = PersonInfo.objects.get(user=user)
    return render(response, 'main/customer/index.html', {
        'user': user,
        'person': person,
    })  # Customer


@login_required
def customerEditProfile(response, id):
    user = get_object_or_404(User, id=id)
    person = PersonInfo.objects.get(user=user)
    if response.method == "POST":
        user.first_name = response.POST['fname']
        user.last_name = response.POST['lname']
        user.email = response.POST['email']
        user.save()
        person.address = response.POST['address']
        person.dob = response.POST['dob']
        person.contact = response.POST['contact']
        person.save()
        messages.success(response, 'Successfully updated your profile!')
        return redirect('customer_index')
    return render(response, 'main/customer/editprofile.html', {
        'user': user,
        'person': person,
    })  # Customer


@login_required
def customerChangePicture(response, id):
    user = User.objects.get(id=id)
    person = PersonInfo.objects.get(user=user)
    if response.method == "POST":
        person.image = response.FILES.get('image')
        person.save()
        messages.success(response, 'Successfully changed profile picture!')
        return redirect('customer_index')
    return render(response, 'main/customer/changepicture.html', {
        'person': person,
    })  # Customer


@login_required
def customerCancelOrder(response, id):
    trans = Transaction.objects.get(id=id)
    trans.delete()
    orders = Order.objects.filter(transaction_id=trans.transaction_id)
    for order in orders:
        ords = Order.objects.get(id=order.id)
        ords.delete()
    messages.error(response, 'Order has been cancelled!')
    return redirect('customer_pending_order')


@login_required
def customerPendingOrder(response):
    user = response.user
    transaction = Transaction.objects.filter(
        user=user, status='Pending') | Transaction.objects.filter(user=user, status='Cancelled')
    return render(response, 'main/customer/pendingorderlist.html', {
        'transaction': transaction,
    })  # Customer


@login_required
def customerProcessOrder(response):
    user = response.user
    trans = Transaction.objects.filter(
        user=user, status='In-Process') | Transaction.objects.filter(user=user, status='Out for Delivery')
    return render(response, 'main/customer/inprocessorder.html', {
        'trans': trans,
    })  # Customer


@login_required
def customerCompletedOrder(response):
    user = response.user
    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    trans = Transaction.objects.filter(
        Q(user=user, status='Completed', date_created__icontains=formatted_date)
    )
    return render(response, 'main/customer/completedorder.html', {
        'trans': trans,
    })


@login_required
def customerHistoryOrder(response):
    user = response.user
    orders = Order.objects.filter(user=user, status='Cancelled') | Order.objects.filter(
        user=user, status='Completed')
    return render(response, 'main/customer/orderhistory.html', {
        'orders': orders,
    })  # Customer


@login_required
def customerFeedback(response):
    id = response.POST.get('id')
    order = Order.objects.get(id=id)
    product = ProductInfo.objects.get(id=order.product.id)
    user = response.user
    if response.method == "POST":
        feedback = response.POST.get('message')
        rate = response.POST.get('rate')
        if feedback == '':
            messages.error(response, 'Please fill the message field! ')
            return redirect('customer_view_rate_order', order.transaction_id)

        feedback_data = FeedBack(
            user=user, order=order, message=feedback, rating=rate)
        if feedback_data.rating == None:
            messages.error(response, 'Please fill the star rating! ')
            return redirect('customer_view_rate_order', order.transaction_id)
        feedback_data.save()
        add = float(product.ratings) + float(rate)
        div = float(add) / 2
        product.ratings = div
        product.save()
        order.is_rated = True
        order.save()
        messages.success(response, 'Feedback has been submitted!')
        return redirect('customer_view_rate_order', order.transaction_id)


def customerViewOrderList(response, trans_id):
    trans = Transaction.objects.filter(transaction_id=trans_id)
    orders = Order.objects.filter(transaction_id=trans_id, status='Pending') | Order.objects.filter(
        transaction_id=trans_id, status='Cancelled')

    return render(response, 'main/customer/viewitemlist.html', {
        'orders': orders,
        'trans': trans,
        'total_amount': sum(order.total_amount for order in orders)
    })


def customerViewOrderListInProcess(response, trans_id):
    trans = Transaction.objects.filter(transaction_id=trans_id)
    orders = Order.objects.filter(transaction_id=trans_id, status='In-Process') | Order.objects.filter(
        transaction_id=trans_id, status='Out for Delivery')

    return render(response, 'main/customer/viewitemlist.html', {
        'orders': orders,
        'trans': trans,
        'total_amount': sum(order.total_amount for order in orders)
    })


def customerSingleOrder(response):
    user = response.user
    orders = Order.objects.filter(user=user, status='Single-Order')
    if response.method == "POST":
        for order in orders:
            ords = get_object_or_404(Order, id=order.id)
            break
        transaction = Transaction(
            user=user, total_amount=ords.total_amount, transaction_id=ords.transaction_id)
        if response.POST.get('mode') == 'Dine-In':
            transaction.order_mode = response.POST.get('mode')
            transaction.status = 'Pending'
            transaction.save()
            ords.status = 'Pending'
            ords.save()
            return redirect('main_food_success')
        else:
            if response.POST.get('location') == '':
                messages.error(response, 'Please fill the address field! ')
                return redirect('customer_single_order')

            transaction.address = response.POST.get('location')
            transaction.order_mode = response.POST.get('mode')
            transaction.status = 'Pending'
            transaction.save()
            ords.status = 'Pending'
            ords.save()
            return redirect('main_food_success')
    return render(response, 'main/pages/singleorder.html', {
        'orders': orders,
    })


def customerSummaryOrder(response):
    user = response.user
    if Order.objects.filter(user=user, status='In-Summary'):
        print('done')
        orders = Order.objects.filter(user=user, status='In-Summary')
        for order in orders:
            ords = Order.objects.get(id=order.id)
            break

        transaction = get_object_or_404(
            Transaction, transaction_id=ords.transaction_id)
        transaction.total_amount = 0
        transaction.save()
        for order in orders:
            total_order = transaction.total_amount + order.total_amount
            transaction.total_amount = total_order
            transaction.save()
        if response.method == "POST":
            if response.POST.get('mode') == 'Dine-In':
                transaction.order_mode = response.POST.get('mode')
                transaction.status = 'Pending'
                transaction.save()
            else:
                if response.POST.get('location') == '':
                    messages.error(response, 'Please fill the address field! ')
                    return redirect('customer_summary_order')

                transaction.address = response.POST.get('location')
                transaction.order_mode = response.POST.get('mode')
                transaction.status = 'Pending'
                transaction.save()

            for order in orders:
                data = get_object_or_404(Order, id=order.id)
                data.status = 'Pending'
                data.save()
            if Order.objects.filter(user=user, status='In-Cart'):
                orders = Order.objects.filter(user=user, status='In-Cart')
                for order in orders:
                    ords = Order.objects.get(id=order.id)
                    ords.delete()
            return redirect('main_food_success')
    else:
        transaction = ''
        orders = ''

    return render(response, 'main/pages/summaryorder.html', {
        'transaction': transaction,
        'orders': orders,
    })


def customerRateViewOrder(response, trans_id):
    trans = Transaction.objects.filter(transaction_id=trans_id)
    orders = Order.objects.filter(transaction_id=trans_id, status='Completed')
    return render(response, 'main/customer/rateviewitemlist.html', {
        'trans': trans,
        'orders': orders,
        'total_amount': sum(order.total_amount for order in orders)
    })

# def customerContactUs(response):
