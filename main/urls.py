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
    path("v1/cat/list", views.adminCatList, name="admin_cat_list"),
    path("v1/<path:str>/food", views.adminFoodCat, name="admin_food_cat"),
    path("v1/food/create", views.adminFoodCreate, name="admin_food_create"),
    path("v1/food/edit/<int:id>", views.adminFoodEdit, name='admin_food_edit'),
    path("v1/food/delete/<int:id>",
         views.adminFoodDelete, name='admin_food_delete'),
    path("v1/feedback/list", views.adminViewFeedback, name="admin_feedback_list"),
    # Customer
    path("v2/", views.customerIndex, name="customer.index"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
