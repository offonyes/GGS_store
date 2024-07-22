from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from accounts_app.models import CustomUser
from accounts_app.forms import RegisterForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = RegisterForm
    model = CustomUser
    list_display = ["email", "first_name", "last_name", "is_staff"]
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


admin.site.unregister(Group)
