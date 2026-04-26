from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Food, Hotel, Order


# 🏠 HOME
def home(request):
    return render(request, 'home.html')


# 📄 STATIC PAGES
def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


# 🏨 HOTEL LIST
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels/hotel_list.html', {'hotels': hotels})


# 🏨 HOTEL DETAIL
def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    # 🔥 Show only rescue foods
    foods = Food.objects.filter(hotel=hotel, is_rescue=True)

    return render(request, 'hotels/hotel_detail.html', {
        'hotel': hotel,
        'foods': foods
    })


# 🍔 FOOD DETAIL
def food_detail(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    return render(request, 'orders/food_detail.html', {
        'food': food
    })


# 🔥 RESCUE DEALS
def rescue_deals(request):
    foods = Food.objects.select_related("hotel").filter(is_rescue=True)

    return render(request, "hotels/rescue_deals.html", {
        "foods": foods
    })


# 🛒 ADD TO CART
def add_to_cart(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    cart = request.session.get('cart', {})

    if str(food_id) in cart:
        cart[str(food_id)] += 1
    else:
        cart[str(food_id)] = 1

    request.session['cart'] = cart

    return redirect('cart_page')


# 🛒 CART PAGE
def cart_page(request):
    cart = request.session.get('cart', {})
    foods = []
    total = 0

    for food_id, qty in cart.items():
        food = get_object_or_404(Food, id=food_id)
        food.qty = qty
        food.total_price = qty * float(food.discounted_price)

        total += food.total_price
        foods.append(food)

    return render(request, 'orders/cart.html', {
        'foods': foods,
        'total': total
    })


# 💳 CHECKOUT
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart_page')

    total = 0
    for food_id, qty in cart.items():
        food = get_object_or_404(Food, id=food_id)
        total += qty * float(food.discounted_price)

    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        upi_id = request.POST.get('upi_id')

        # ⚠️ Validation
        if not payment_method:
            return render(request, 'hotels/checkout.html', {
                'total': total,
                'error': 'Please select a payment method'
            })

        if payment_method == "UPI" and not upi_id:
            return render(request, 'hotels/checkout.html', {
                'total': total,
                'error': 'Please enter your UPI ID'
            })

        # ✅ Create Order
        order = Order.objects.create(
            name=name,
            phone=phone,
            address=address,
            total_price=total,
            payment_method=payment_method,
            is_paid=False
        )

        # 💰 COD
        if payment_method == "COD":
            request.session['cart'] = {}
            return redirect('thank_you', order_id=order.id)

        # 📱 UPI
        elif payment_method == "UPI":
            return redirect('upi_payment', order_id=order.id)

    return render(request, 'hotels/checkout.html', {
        'total': total
    })


# 📱 UPI PAYMENT
def upi_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    upi_link = f"upi://pay?pa=lastcalleats@upi&pn=LastCallEats&am={order.total_price}&cu=INR"

    return render(request, "hotels/upi_payment.html", {
        "order": order,
        "upi_link": upi_link
    })


# ✅ CONFIRM UPI PAYMENT
def confirm_upi_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    order.is_paid = True
    order.save()

    return redirect('thank_you', order_id=order.id)


# 🎉 THANK YOU
def thank_you(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'hotels/thank_you.html', {
        'order': order
    })


# 🔐 CREATE / RESET ADMIN (TEMPORARY - VERY IMPORTANT)
def create_admin(request):
    try:
        user = User.objects.get(username="admin")
        user.set_password("admin123")  # 🔥 reset password
        user.save()
        return HttpResponse("✅ Password reset → admin / admin123")
    except User.DoesNotExist:
        return HttpResponse("❌ Admin user not found")