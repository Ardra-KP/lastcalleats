from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('food/<int:food_id>/', views.food_detail, name='food_detail'),
    path('<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('rescue-deals/', views.rescue_deals, name='rescue_deals'),
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_page, name='cart_page'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm-payment/<int:order_id>/', views.confirm_upi_payment, name='confirm_upi_payment'),
    path('thank-you/', views.thank_you, name='thank_you'),

]
