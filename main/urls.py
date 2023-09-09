from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    # Admin
    path("v1/", views.adminIndex, name="admin.index"),
    path("v1/cat/list", views.adminCatList, name="admin.cat.list"),
    path("v1/food/list", views.adminFoodList, name="admin.food.list"),
    path("v1/food/create", views.adminFoodCreate, name="admin.food.create"),
    # Customer
    path("v2/", views.customerIndex, name="customer.index"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
