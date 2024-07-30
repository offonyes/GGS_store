from django.contrib import admin
from django.db.models import Count, Q, Sum, F, Case, When

from shoe_app.models import Shoe, Category, Review
from shoe_app.filters import CategoryFilter, ShoeFilter, UserFilter
from accounts_app.models import CustomUser


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'shoe_count']
    search_fields = ['name']
    list_filter = ['gender']
    readonly_fields = ['shoe_count']
    show_full_result_count = False
    fieldsets = ((None, {'fields': (('name', 'gender'), 'shoe_count')}),)

    def shoe_count(self, obj):
        return obj.shoe_count

    shoe_count.short_description = 'Shoe Count'
    shoe_count.admin_order_field = 'shoe_count'


@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    list_display = ['name', 'base_price', 'sales_count', 'total_profit', 'review_avg']
    search_fields = ['name']
    list_filter = [CategoryFilter]
    readonly_fields = ['sales_count', 'total_profit', 'review_avg']
    show_full_result_count = False
    fieldsets = (('Main Information', {'fields': (('category', 'name'), ('base_price', 'discount_price'), 'image',
                                                  'description')}),
                 ('Statistic', {'fields': (('sales_count', 'total_profit'), 'review_avg'),
                                'classes': ('collapse',)}))

    def get_queryset(self, request):
        return (super(ShoeAdmin, self)
                .get_queryset(request).select_related('category')
                .annotate(sales_count=Sum('orderitems__quantity'),
                          total_profit=Sum(F('orderitems__quantity') * F('orderitems__price')))
                .defer(*{f'category__{x.name}' for x in Category._meta.fields if x.name not in {'name'}}))

    def sales_count(self, obj):
        return obj.sales_count

    sales_count.short_description = 'Sales Count'
    sales_count.admin_order_field = 'sales_count'

    def total_profit(self, obj):
        return obj.total_profit

    total_profit.short_description = 'Total Profit'
    total_profit.admin_order_field = 'total_profit'

    def review_avg(self, obj):
        return obj.review_avg

    review_avg.short_description = 'Review Average'
    review_avg.admin_order_field = 'review_avg'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user', 'shoe']
    date_hierarchy = 'created_at'
    list_display = ['user', 'shoe', 'created_at', 'rating']
    list_filter = [ShoeFilter, UserFilter, 'rating']
    show_full_result_count = False

    def get_queryset(self, request):
        return (super(ReviewAdmin, self)
                .get_queryset(request).select_related('user', 'shoe')
                .defer(*{f'user__{x.name}' for x in CustomUser._meta.fields if x.name not in {'email'}})
                .defer(*{f'shoe__{x.name}' for x in Shoe._meta.fields if x.name not in {'name'}}))
