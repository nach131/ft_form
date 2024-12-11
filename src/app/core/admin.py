"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _
from django import forms
import requests
from django.conf import settings
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from django.db import transaction

from core import models
from .models import (Form, TextQuestion, BooleanQuestion, OptionQuestion, MultipleChoiceQuestion,
                    EmailQuestion, NumberQuestion, ScaleQuestion, DateQuestion, URLQuestion,
                    FileQuestion, SentForm, Campus, Cursus)

# Acción que permite duplicar un formulario
@admin.action(description='Duplicate a Form')
def duplicate_form(modeladmin, request, queryset):
    for form in queryset:
        # transaction atomic asegura que todas las operaciones dentro del bloque se ejecuten
        #por completo y, si ocurre un error, se deshacen todas juntas
        with transaction.atomic():
            original_form = form
            new_form = Form.objects.create(
                name = f"{form.name} (copia)",
                favourite = form.favourite,
                message_end_form = form.message_end_form,
                image = form.image
            )

            for question_model in [TextQuestion, BooleanQuestion, OptionQuestion, MultipleChoiceQuestion,
                                   EmailQuestion, NumberQuestion, ScaleQuestion, DateQuestion, URLQuestion,
                                   FileQuestion]:
                questions = question_model.objects.filter(form_id=original_form)
                for question in questions:
                    question.id = None
                    question.form_id = new_form
                    question.save()


class TextQuestionInLine(admin.TabularInline):
    model = TextQuestion
    extra = 1

class BooleanQuestionInLine(admin.TabularInline):
    model = BooleanQuestion
    extra = 1

class OptionQuestionInLine(admin.TabularInline):
    model = OptionQuestion
    extra = 1

class MultipleChoiceQuestionInLine(admin.TabularInline):
    model = MultipleChoiceQuestion
    extra = 1

class NumberQuestionInLine(admin.TabularInline):
    model = NumberQuestion
    extra = 1

class EmailQuestionInLine(admin.TabularInline):
    model = EmailQuestion
    extra = 1

class ScaleQuestionInLine(admin.TabularInline):
    model = ScaleQuestion
    extra = 1

class DateQuestionInLine(admin.TabularInline):
    model = DateQuestion
    extra = 1

class URLQuestionInLine(admin.TabularInline):
    model = URLQuestion
    extra = 1
    
class FileQuestionInLine(admin.TabularInline):
    model = FileQuestion
    extra = 1

class   FormAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

    inlines = [TextQuestionInLine, BooleanQuestionInLine, OptionQuestionInLine, EmailQuestionInLine,
            ScaleQuestionInLine, DateQuestionInLine, URLQuestionInLine, FileQuestionInLine,
            MultipleChoiceQuestionInLine, NumberQuestionInLine]
    actions = [duplicate_form]
    

admin.site.register(Form, FormAdmin)
admin.site.add_action(duplicate_form)
admin.site.register(TextQuestion)
admin.site.register(BooleanQuestion)
admin.site.register(OptionQuestion)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(NumberQuestion)
admin.site.register(EmailQuestion)
admin.site.register(ScaleQuestion)
admin.site.register(DateQuestion)
admin.site.register(URLQuestion)
admin.site.register(FileQuestion)
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

class ExternalAPIForm(forms.Form):
    TOKEN_URL = "https://api.intra.42.fr/oauth/token"
    EXTERNAL_API_URL = None

    def __init__(self, *args, **kwargs):
        self.EXTERNAL_API_URL = kwargs.pop("api_url", "")
        super().__init__(*args, **kwargs)
        self.fields['choices'].choices = self.fetch_data()

    def authenticate(self):
        """
        Authenticates using OAuth2 with the Client Credentials grant type.
        Returns an authenticated session.
        """
        # Set up the OAuth2 client and session
        client = BackendApplicationClient(client_id=settings.UID)
        oauth = OAuth2Session(client=client)

        # Fetch token from the token endpoint
        token = oauth.fetch_token(
            token_url=self.TOKEN_URL,
            client_secret=settings.SECRET
        )
        return oauth

    def fetch_data(self):
        """
        Fetch paginated data using an authenticated session and handle pagination.
        """
        try:
            session = self.authenticate()
            all_choices = []
            page_number = 1
            page_size = 100  # You can modify this based on your requirements

            #while True:
            response = session.get(
                self.EXTERNAL_API_URL,
                params={"page[number]": page_number, "page[size]": page_size}
            )
            response.raise_for_status()
            data = response.json()
            # Handle list response directly if it's a list
            if isinstance(data, list):
                for item in data:
                    if 'id' in item and 'name' in item:
                        all_choices.append((f"{item['id']}|{item['name']}", item['name']))

            # Handle paginated response with 'data' key
            elif 'data' in data and isinstance(data['data'], list):
                for item in data['data']:
                    if 'id' in item and 'name' in item:
                        all_choices.append((f"{item['id']}|{item['name']}", item['name']))

            # Break loop if no new data is found
            #if not data or len(data) < page_size:
            #    break
            print(data)
            page_number += 1

            return all_choices
        except Exception as e:
            print(f"Error fetching paginated data: {e}")
            return []

    choices = forms.ChoiceField(choices=[], label="Select Options")

# Step 3: Admin customization for Campus and Cursus
class CampusAdminForm(forms.ModelForm):

    external_choice = forms.ChoiceField(choices=[], label="Select Campus")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        api_form = ExternalAPIForm(api_url="https://api.intra.42.fr/v2/campus")
        self.fields['external_choice'].choices = api_form.fetch_data()

    class Meta:
        model = Campus
        fields = ['external_choice']

    # Handling data transformation during save
    def save(self, commit=True):
        obj = super().save(commit=False)
        if 'external_choice' in self.cleaned_data:
            id_42, name = self.cleaned_data['external_choice'].split('|')
            obj.id_42 = int(id_42)
            obj.name = name
        if commit:
            obj.save()
        return obj


class CursusAdminForm(forms.ModelForm):

    external_choice = forms.ChoiceField(choices=[], label="Select Cursus")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        api_form = ExternalAPIForm(api_url="https://api.intra.42.fr/v2/cursus")
        self.fields['external_choice'].choices = api_form.fetch_data()

    class Meta:
        model = Cursus
        fields = ['external_choice']

    # Handling data transformation during save
    def save(self, commit=True):
        obj = super().save(commit=False)
        if 'external_choice' in self.cleaned_data:
            id_42, name = self.cleaned_data['external_choice'].split('|')
            obj.id_42 = int(id_42)
            obj.name = name
        if commit:
            obj.save()
        return obj


# Admin Registration
class CampusAdmin(admin.ModelAdmin):
    form = CampusAdminForm


class CursusAdmin(admin.ModelAdmin):
    form = CursusAdminForm


admin.site.register(Campus, CampusAdmin)
admin.site.register(Cursus, CursusAdmin)