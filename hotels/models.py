from django.db import models
from django.utils import timezone
from decimal import Decimal


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="hotels/", blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    # Available foods for this hotel
    def available_foods(self):
        return self.foods.filter(
            available=True,
            available_until__gt=timezone.now()
        )


class Food(models.Model):

    CATEGORY_CHOICES = [
        ("veg", "Veg"),
        ("nonveg", "Non-Veg"),
        ("biryani", "Biryani"),
        ("dessert", "Dessert"),
        ("snack", "Snack"),
    ]

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="foods"
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="veg"
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00")
    )

    discount_percentage = models.PositiveIntegerField(default=50)

    image = models.ImageField(
        upload_to="foods/",
        default="foods/placeholder.jpg",
        blank=True
    )

    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.2)

    # Meals stock
    quantity_left = models.PositiveIntegerField(default=5)

    is_rescue_food = models.BooleanField(default=True)

    available_until = models.DateTimeField()

    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    # 🔥 Discounted Price
    @property
    def discounted_price(self):
        discount_amount = (self.discount_percentage / 100) * float(self.price)
        return Decimal(self.price) - Decimal(discount_amount)

    # 🟢 Check if food is available
    @property
    def is_available_now(self):
        return (
            self.available
            and timezone.now() < self.available_until
            and self.quantity_left > 0
        )

    # 🔥 Discount badge
    @property
    def badge_label(self):
        if self.is_rescue_food:
            return f"{self.discount_percentage}% OFF"
        return ""

    # ⏳ Time remaining
    @property
    def time_remaining(self):
        if self.available_until > timezone.now():
            return self.available_until - timezone.now()
        return None

    # 🔥 Meals left label
    @property
    def meals_left_label(self):
        if self.quantity_left > 0:
            return f"🔥 Only {self.quantity_left} meals left"
        return "Sold Out"

    def __str__(self):
        return f"{self.name} - {self.hotel.name}"


# 🔥 NEW: ORDER MODEL (PAYMENT SYSTEM)
class Order(models.Model):

    PAYMENT_CHOICES = [
        ("COD", "Cash on Delivery"),
        ("UPI", "UPI / Google Pay"),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    total_price = models.FloatField()

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES
    )

    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.name} ({self.payment_method})"