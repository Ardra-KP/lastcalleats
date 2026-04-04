from django.urls import path
from .views import order_food, views

urlpatterns = [
    path('<int:food_id>/', order_food, name='order_food'),
]
