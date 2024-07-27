from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db.models import Count, Q, Sum, F, Case, When

from accounts_app.models import CustomUser
from accounts_app.forms import RegisterForm
from order_app.choice import StatusChoices


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = RegisterForm
    model = CustomUser
    list_display = ["email", "first_name", "last_name", "is_staff", "total_orders", "total_spent"]
    list_filter = ["is_staff"]
    fieldsets = (
        ("Account Information", {"fields": (("email", "password"),), "classes": ("wide",),
                                 "description": "User Details"}),
        ("Personal Info", {"fields": (("first_name", "last_name"), ("personal_number", "birth_date"), "phone_number",
                                      "date_joined"),
                           "classes": ("collapse",),
                           "description": "Personal information about user"}),
        ("Permissions",
         {"fields": (("is_active", "is_staff"), "groups", "user_permissions"),
          "classes": ("collapse",)},),
    )
    add_fieldsets = (
        ("Account Information", {"fields": ("email", "password1", "password2",), "classes": ("wide",)}),
        ("Personal Info", {"fields": (("first_name", "last_name"), ("personal_number", "birth_date"), "phone_number")}),
        ("Permissions", {"fields": (("is_active", "is_staff"), "groups", "user_permissions")},)
    )
    search_fields = ["email", "first_name", "last_name", "personal_number"]
    ordering = ["email"]
    readonly_fields = ["date_joined"]

    def get_queryset(self, request):
        return (super(UserAdmin, self).get_queryset(request)
                .annotate(total_orders=Count('order',
                          filter=Q(order__status__in=[StatusChoices.PENDING, StatusChoices.PROCESSING,
                                                      StatusChoices.COMPLETED]), distinct=True),
                          total_spent=Sum(F('order__orderitems__quantity') * F('order__orderitems__price'), distinct=True))
                )

    def total_orders(self, obj):
        return obj.total_orders

    total_orders.short_description = "Total Orders"
    total_orders.admin_order_field = 'total_orders'

    def total_spent(self, obj):
        return obj.total_spent

    total_spent.short_description = "Total Spent"
    total_spent.admin_order_field = 'total_spent'


admin.site.unregister(Group)
