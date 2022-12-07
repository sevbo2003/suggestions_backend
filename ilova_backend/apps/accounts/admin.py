from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from .models import CustomUser


# class CustomUserAdmin(UserAdmin):
    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     (_('Permissions'), {
    #         'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
    #     }),
    #     (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    # )
    # list_display = ('username', 'is_verified', 'is_staff')
    # search_fields = ('username',)
    # ordering = ('username',)
    # filter_horizontal = ('groups', 'user_permissions',)
    # list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'is_verified')


admin.site.register(CustomUser)
            