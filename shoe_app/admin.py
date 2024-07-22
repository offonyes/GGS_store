from django.contrib import admin

from shoe_app.models import Shoe, Category, ShoeSize, Review
from shoe_app.filters import CategoryFilter, ShoeFilter, SizeFilter, UserFilter


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender']
    search_fields = ['name']
    list_filter = ['gender']


# class ShoeSizeInline(admin.TabularInline):
        # model = BooksBorrow
        # verbose_name = _('Book Borrowing History')
        # verbose_name_plural = _('Book Borrowing Histories')
        # can_delete = False
        # per_page = 10
        # max_num = 0
        # readonly_fields = ['book', 'borrower', 'borrowed_status', 'borrowed_date', 'return_date']
        #
        # def get_queryset(self, request):
        #     return super(BooksInline, self).get_queryset(request).select_related(
        #         'book', 'borrower')


@admin.register(ShoeSize)
class ShoeSizeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['shoe']
    list_display = ['shoe', 'size', 'available_amount']
    search_fields = ['shoe']
    list_filter = [ShoeFilter, 'available_amount']


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
