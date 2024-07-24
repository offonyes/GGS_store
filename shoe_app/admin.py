from django.contrib import admin

from shoe_app.models import Shoe, Category, Review
from shoe_app.filters import CategoryFilter, ShoeFilter, UserFilter


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender']
    search_fields = ['name']
    list_filter = ['gender']


@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    list_display = ['name', 'category', 'base_price']
    search_fields = ['name']
    list_filter = [CategoryFilter]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user', 'shoe']
    date_hierarchy = 'created_at'
    list_display = ['user', 'shoe', 'created_at', 'rating']
    list_filter = [ShoeFilter, UserFilter, 'rating']
