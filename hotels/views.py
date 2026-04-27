from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel, Food, Order


# 🏠 HOME
def home(request):
    return render(request, 'home.html')


# 📄 ABOUT
def about(request):
    return render(request, 'about.html')


# 📄 CONTACT
def contact(request):
    return render(request, 'contact.html')


# 🏨 HOTEL LIST
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels/hotel_list.html', {'hotels': hotels})


# 🏨 HOTEL DETAIL
def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    # ✅ Only available foods
    foods = hotel.available_foods()

    return render(request, 'hotels/hotel_detail.html', {
        'hotel': hotel,
        'foods': foods
    })


# 🍔 FOOD DETAIL
def food_detail(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    return render(request, 'orders/food_detail.html', {'food': food})

# 🛒 ADD TO CART
def add_to_cart(request, food_id):
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

def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart_page')

    total = 0
    foods = []

    for food_id, qty in cart.items():
        food = get_object_or_404(Food, id=food_id)
        food.qty = qty
        food.total_price = qty * float(food.discounted_price)

        total += food.total_price
        foods.append(food)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        payment_method = request.POST.get("payment_method")

        order = Order.objects.create(
            name=name,
            phone=phone,
            address=address,
            total_price=total,
            payment_method=payment_method,
            is_paid=(payment_method == "COD")
        )

        # ✅ COD → clear cart here
        if payment_method == "COD":
            request.session['cart'] = {}
            return redirect('thank_you', order_id=order.id)

        # ✅ UPI → go to payment page (DON'T clear cart yet)
        return redirect('upi_payment', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'foods': foods,
        'total': total
    })

def upi_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'orders/upi_payment.html', {
        'order': order
    })

def thank_you(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'orders/thank_you.html', {
        'order': order
    })
def confirm_upi_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    order.is_paid = True
    order.save()

    # ✅ NOW clear cart AFTER payment
    request.session['cart'] = {}

    return redirect('thank_you', order_id=order.id)

def rescue_deals(request):
    foods = Food.objects.filter(
        is_rescue_food=True,
        available=True
    ).order_by('-created_at')

    return render(request, 'hotels/rescue_deals.html', {
        'foods': foods
    })