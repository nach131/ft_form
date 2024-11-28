"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name',  'is_active', 'is_cancel','is_42_staf']
    list_filter = ['is_active', 'is_cancel']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': (
            'name',
        )}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_cancel',
                    'is_staff',
                    'is_superuser',
                                    'is_42_staf',

                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login', 'last_activity')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )
