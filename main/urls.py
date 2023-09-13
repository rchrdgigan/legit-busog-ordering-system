from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("changepassword/", views.changePassword, name='change_password'),
    # Admin
    path("v1/", views.adminIndex, name="admin.index"),
    path("v1/cat/list", views.adminCatList, name="admin_cat_list"),
    path("v1/cat/update", views.adminCatUpdate, name='admin_cat_update'),
    path("v1/food/<int:id>", views.adminFoodCat, name="admin_food_cat"),
    path("v1/food/create/<int:id>",
         views.adminFoodCreate, name="admin_food_create"),
    path("v1/food/edit/<int:id>", views.adminFoodEdit, name='admin_food_edit'),
    path('v1/food/available/<int:ida>/<int:id>',
         views.adminFoodAvailable, name='admin_food_available'),
    path('v1/food/unavailable/<int:ida>/<int:id>',
         views.adminFoodUnavailable, name='admin_food_unavailable'),
    path("v1/food/delete/<int:id2>/<int:id>",
         views.adminFoodDelete, name='admin_food_delete'),
    path("v1/feedback/list", views.adminViewFeedback, name="admin_feedback_list"),
    path("v1/account/list", views.adminViewAccount, name="admin_account_list"),
    # Customer
    path("v2/", views.customerIndex, name="customer.index"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
