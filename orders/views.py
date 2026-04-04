from django.shortcuts import render, redirect

# Create your views here.

from hotels.models import Food
from .models import Order

def order_food(request, food_id):
    food = Food.objects.get(id=food_id)

    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        Order.objects.create(
            food=food,
            customer_name=request.POST['customer_name'],
            quantity=quantity,
            total_price=food.price * quantity
        )
        return redirect('/')

    return render(request, 'orders/order_food.html', {'food': food})

def checkout(request):
    cart = request.session.get('cart', {})

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        # Save each cart item as order
        for food_id, qty in cart.items():
            food = Food.objects.get(id=food_id)

            Order.objects.create(
                food=food,
                customer_name=name,
                phone=phone,
                address=address,
                quantity=qty
            )

        # 🔥 Clear cart after order
        request.session['cart'] = {}

        return render(request, "orders/success.html")

    return render(request, "orders/checkout.html")

