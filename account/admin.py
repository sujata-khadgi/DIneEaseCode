from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from account.models import Product

from .forms import UserAdminCreationForm, UserAdminChangeForm
User = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = UserAdminCreationForm
    form = UserAdminChangeForm
    model = User
    list_display = ("email", "is_active","admin")
    list_filter = ("email", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ( "is_active","staff","admin","customer","driver")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password", "password_2", "staff","admin",
                "is_active"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()

admin.site.register(User, CustomUserAdmin)

admin.site.register(Product)