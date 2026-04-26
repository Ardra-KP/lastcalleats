from django.urls import path
from . import views

urlpatterns = [

    # 🔐 ADMIN (PUT THIS AT TOP)
    path('create-admin/', views.create_admin, name='create_admin'),

    # 🏠 Hotels
    path('', views.hotel_list, name='hotel_list'),

    # 🍔 Food
    path('food/<int:food_id>/', views.food_detail, name='food_detail'),

    # 🔥 Deals
    path('rescue-deals/', views.rescue_deals, name='rescue_deals'),

    # 🛒 Cart
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_page, name='cart_page'),

    # 💳 Checkout
    path('checkout/', views.checkout, name='checkout'),

    # 📱 Payment
    path('upi-payment/<int:order_id>/', views.upi_payment, name='upi_payment'),
    path('confirm-payment/<int:order_id>/', views.confirm_upi_payment, name='confirm_upi_payment'),

    # 🎉 Success
    path('thank-you/<int:order_id>/', views.thank_you, name='thank_you'),

    # 🏨 HOTEL DETAIL (⚠️ ALWAYS KEEP THIS LAST)
    path('<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
]