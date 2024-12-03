"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _

from core import models
from .models import Form, TextQuestion, BooleanQuestion, OptionQuestion, SentForm

class TextQuestionInLine(admin.TabularInline):
    model = TextQuestion
    extra = 1

class BooleanQuestionInLine(admin.TabularInline):
    model = BooleanQuestion
    extra = 1

class OptionQuestionInLine(admin.TabularInline):
    model = OptionQuestion
    extra = 1

class   FormAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

    inlines = [TextQuestionInLine, BooleanQuestionInLine, OptionQuestionInLine]

admin.site.register(Form, FormAdmin)
admin.site.register(TextQuestion)
admin.site.register(BooleanQuestion)
admin.site.register(OptionQuestion)
admin.site.register(SentForm)

#admin.site.register(User)

@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'username',  'is_active', 'is_cancel','is_42_staf']
    list_filter = ['is_active', 'is_cancel']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': (
            'username',
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
                'username',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )
