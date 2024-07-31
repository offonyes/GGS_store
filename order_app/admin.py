from django.contrib import admin
from django.db.models import F

from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter

from shoe_app.filters import ShoeFilter, UserFilter
from order_app.filters import OrderFilter, CartFilter
from order_app.models import Order, OrderItem, Cart, CartItem
from accounts_app.models import CustomUser

admin.site.site_header = "GGS Admin"
admin.site.site_title = "GGS Admin Page"
admin.site.index_title = "Welcome to GGS Admin Page"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['user', 'status', 'items', 'total_price']
    search_fields = ['user']
    list_filter = [UserFilter, 'status']
    date_hierarchy = 'date_ordered'
    list_editable = ['status']
    readonly_fields = ['date_ordered', 'items', 'total_price']
    show_full_result_count = False
    fieldsets = ((None, {'fields': ('user', ('date_ordered', 'status'))}),
                 ('Additional Information', {'fields': (('items', 'total_price'),)}))

    def get_queryset(self, request):
        return (super(OrderAdmin, self)
                .get_queryset(request).select_related('user')
                .defer(*{f'user__{x.name}' for x in CustomUser._meta.fields if x.name not in {'email'}}))

    def items(self, obj):
        return obj.items

    items.short_description = 'Items'
    items.admin_order_field = 'items'

    def total_price(self, obj):
        return obj.total_price

    total_price.short_description = 'Total Price'
    total_price.admin_order_field = 'total_price'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['order', 'shoe']
    list_display = ['order', 'shoe', 'size', 'price', 'quantity']
    list_filter = [ShoeFilter, OrderFilter, ('size', DropdownFilter), ('color', DropdownFilter)]
    date_hierarchy = 'date_added'
    readonly_fields = ['date_added']
    show_full_result_count = False
    fieldsets = ((None, {'fields': (('order', 'shoe'), ('size', 'color'), ('price', 'quantity'), 'date_added'),
                         'classes': ('wide',)}),)

    def get_queryset(self, request):
        return (super(OrderItemAdmin, self)
                .get_queryset(request).select_related('order', 'shoe', 'order__user')
                .defer(*{f'order__user__{x.name}' for x in CustomUser._meta.fields if x.name not in {'email'}}))


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['user', 'items', 'total_price']
    search_fields = ['user']
    list_filter = [UserFilter]
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'items', 'total_price']
    show_full_result_count = False
    fieldsets = ((None, {'fields': ('user', 'created_at')}),
                 ('Additional Information', {'fields': (('items', 'total_price'),)}))

    def get_queryset(self, request):
        return (super(CartAdmin, self)
                .get_queryset(request).select_related('user')
                .defer(*{f'user__{x.name}' for x in CustomUser._meta.fields if x.name not in {'email'}}))

    def items(self, obj):
        return obj.items

    items.short_description = 'Items'
    items.admin_order_field = 'items'

    def total_price(self, obj):
        return obj.total_price

    total_price.short_description = 'Total Price'
    total_price.admin_order_field = 'total_price'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['cart', 'shoe']
    list_display = ['cart', 'shoe', 'size', 'color', 'quantity']
    list_filter = [ShoeFilter, CartFilter, ('size', DropdownFilter), ('color', DropdownFilter)]
    date_hierarchy = 'date_added'
    readonly_fields = ['date_added']
    show_full_result_count = False
    fieldsets = ((None, {'fields': (('cart', 'shoe'), ('size', 'color'), ('price', 'quantity'), 'date_added'),
                         'classes': ('wide',)}),)

    def get_queryset(self, request):
        return (super(CartItemAdmin, self)
                .get_queryset(request).select_related('cart', 'shoe', 'cart__user')
                .defer(*{f'cart__user__{x.name}' for x in CustomUser._meta.fields if x.name not in {'email'}}))
