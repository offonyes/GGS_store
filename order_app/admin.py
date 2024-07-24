from django.contrib import admin

from shoe_app.filters import CategoryFilter, ShoeFilter, UserFilter
from order_app.models import Order, OrderItem, Cart, CartItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass