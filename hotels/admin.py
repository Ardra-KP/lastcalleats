from django.contrib import admin

# Register your models here.
from .models import Hotel,Food

admin.site.register(Food)
admin.site.register(Hotel)