from django.db import models
from hotels.models import Food

class Order(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)

    # 🔥 Customer details
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    # 📍 Location (GPS)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    quantity = models.PositiveIntegerField(default=1)

    # 💰 Price auto calculation
    total_price = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 🔥 Automatically calculate total price
        self.total_price = self.quantity * float(self.food.discounted_price)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} - {self.food.name}"
