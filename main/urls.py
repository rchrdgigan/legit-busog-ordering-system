from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Main
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("changepassword/", views.changePassword, name='change_password'),
    path("pages/food", views.foodProductList, name="main_food"),
    path("pages/food/show/<int:id>", views.foodProductShow, name="main_food_show"),
    path("pages/food/success", views.foodBuySucessfully, name="main_food_success"),
    path("pages/food/added", views.foodAdded, name="main_food_added"),
    path("pages/viewproduct/category/<int:id>",
         views.ViewProductByCategory, name='view_product_category'),

    # Admin
    path("v1/", views.adminIndex, name="admin.index"),
    path("v1/cat/list", views.adminCatList, name="admin_cat_list"),
    path("v1/cat/update/<int:id>", views.adminCatUpdate, name='admin_cat_update'),
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
    path("v1/account/change_password/<int:id>",
         views.adminUserChangePass, name="admin_account_change_pass"),
    path("v1/order/peding", views.adminPendingOrder,
         name="admin_pending_order"),
    path("v1/order/canceling/<int:id>",
         views.adminCancellingOrder, name="admin_toCancel_order"),
    path("v1/order/to_process/<int:id>",
         views.adminToProcessOrder, name='admin_toProcess_order'),
    path("v1/order/process", views.adminProcessOrder,
         name="admin_process_order"),
    path('v1/order/to_deliver/<int:id>',
         views.adminToDeliverOrder, name='admin_toDeliver_order'),
    path("v1/order/to_complete/<int:id>",
         views.adminToCompleteOrder, name='admin_toComplete_order'),
    path("v1/order/completed", views.adminCompletedOrder,
         name="admin_completed_order"),
    path("v1/order/cancelled", views.adminCancelledOrder,
         name="admin_cancelled_order"),
    path("v1/profile", views.adminProfile, name="admin_profile"),
    path("v1/profile/edit/<int:id>", views.adminEditProfile,
         name="admin_profile_edit"),
    path("v1/profile/change-picture/<int:id>", views.adminChangePicture,
         name="admin_change_picture"),

    path('v1/order/fooodlist/parameter', views.adminViewOrderList,
         name='admin_customer_orderlist'),  # View customer's order list

    path("v1/contact/list", views.adminMessagesList,
         name="admin_messages_list"),

    # Customer
    path("v2/profile", views.customerIndex, name="customer_index"),
    path("v2/profile/edit/<int:id>", views.customerEditProfile,
         name="customer_profile_edit"),
    path("v2/profile/change-picture/<int:id>", views.customerChangePicture,
         name="customer_change_picture"),
    path("v2/order/cancel/<int:id>", views.customerCancelOrder,
         name='customer_cancel_order'),
    path("v2/order/peding", views.customerPendingOrder,
         name="customer_pending_order"),
    path("v2/order/process", views.customerProcessOrder,
         name="customer_process_order"),
    path("v2/order/completed", views.customerCompletedOrder,
         name="customer_completed_order"),
    path("v2/order/history", views.customerHistoryOrder,
         name="customer_history_order"),
    path("v2/order/place-order", views.customerPlaceOrder,  # List of Cart
         name="customer_placeorder_order"),
    path("v2/order/place-order/<int:order_id>", views.customerDeleteOneOrder,  # Delete One Order in Place Order
         name="customer_delete_one_order"),
    path('v2/order/feedback/<int:id>',
         views.customerFeedback, name='customer_feedback'),

    path('v2/order/fooodlist/<int:trans_id>', views.customerViewOrderList,
         name='customer_orderlist'),

    path("v2/order/single-order", views.customerSingleOrder,
         name="customer_single_order"),

    path("v2/order/summary", views.customerSummaryOrder,
         name="customer_summary_order"),

    path("v2/order/view-rate", views.customerRateViewOrder,
         name="customer_view_rate_order"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
