from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('food/<int:food_id>/', views.food_detail, name='food_detail'),
    path('cart/', views.cart_page, name='cart_page'),
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('rescue-deals/', views.rescue_deals, name='rescue_deals'),
    path('upi-payment/<int:order_id>/', views.upi_payment, name='upi_payment'),
    path('confirm-payment/<int:order_id>/', views.confirm_upi_payment, name='confirm_upi_payment'),
    path('thank_you/<int:order_id>/', views.thank_you, name='thank_you'),
]