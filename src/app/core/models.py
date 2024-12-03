"""
Database models.
"""

from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
import os
from django.utils import timezone
from django.db import models
# from django.contrib.postgres.fields import JSONField
from django.db.models import JSONField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

import secrets
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinLengthValidator


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and return a new superuser."""
        user = self.create_user(email, password, **extra_fields)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class SettingsUser(models.Model):

    ejemplo = models.BooleanField(default=False)


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_cancel = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_42_staf = models.BooleanField(default=False)
    role = models.CharField(max_length=50,unique=False, blank=True)
    coalition = JSONField(default=dict)
    level = models.PositiveIntegerField(default=0)
    age = models.PositiveIntegerField(default=0)
    image_url = models.URLField(max_length=200, blank=True, null=True)

    last_activity = models.DateTimeField(null=True, blank=True)


    settings = models.OneToOneField(
        SettingsUser, on_delete=models.CASCADE, related_name="user",
        null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # Campos que son requeridos cuando se crea un superusuario
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def update_last_activity(self):
        self.last_activity = timezone.now()
        self.save()

    def update_online(self, value):
        self.is_online = value
        self.save()

    def save(self, *args, **kwargs):
        # Crear la instancia de SettingsUser si no existe
        if not self.settings:
            settings = SettingsUser.objects.create()
            self.settings = settings
        super(User, self).save(*args, **kwargs)




class Form(models.Model):
    name = models.CharField(max_length=80, verbose_name='Nombre', blank=False, null=False)
    favourite = models.BooleanField(verbose_name='Favorito', default=False)
    message_end_form = models.CharField(max_length=500, verbose_name='Mensaje final', default="Final de formulario")
    image = models.ImageField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Forms'

    def __str__(self):
        return self.name

class TextQuestion(models.Model):
    order = models.IntegerField(verbose_name='pregunta número', blank=False, null=False)
    type = 'Text question'
    max_chars = models.IntegerField(verbose_name='Maximo número de caracteres', default=1000)
    min_chars = models.IntegerField(verbose_name='Mínimo número de caracteres', default=1)
    text = models.CharField(max_length=300, verbose_name='Pregunta', blank=False, null=False)
    is_required = models.BooleanField(verbose_name='¿Respuesta requerida?', default=1)
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Text question'

    def __str__(self):
        return self.text

class BooleanQuestion(models.Model):
    order = models.IntegerField(verbose_name='pregunta número', blank=False, null=False)
    type = 'Boolean question'
    text = models.CharField(max_length=250, verbose_name='Pregunta', blank=False, null=False)
    is_required = models.BooleanField(verbose_name='¿Respuesta requerida?', default=1)
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Boolean question'

    def __str__(self):
        return self.text

class OptionQuestion(models.Model):
    order = models.IntegerField(verbose_name='pregunta número', blank=False, null=False)
    type = 'Option question'
    text = models.CharField(max_length=250, verbose_name='Pregunta', blank=False, null=False)
    options = models.JSONField(default=dict)
    is_required = models.BooleanField(verbose_name='¿Respuesta requerida?', default=1)
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Option question'

    def __str__(self):
        return self.text

class   SentForm(models.Model):
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    sended = models.DateTimeField(verbose_name='sended')
    answered = models.BooleanField(verbose_name='answered', default=False)


# Modelos de respuesta

class Answer(models.Model):
    """Modelo para representar respuestas a preguntas específicas."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="answers")
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    # question = models.ForeignKey(
    #     Question, on_delete=models.CASCADE, related_name="answers"
    # )
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # response = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer from {self.user} to '{self.question}'"

class CharFieldAnswer(models.Model):
    """Modelo para respuestas tipo texto."""
    value = models.CharField(
        max_length=255, blank=True, null=True,
        validators=[MinLengthValidator(3)]
    )
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question_id = models.ForeignKey(TextQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f"CharField Answer: {self.value}"

class BooleanAswer(models.Model):
    """Modelo para respuestas tipo booleano."""
    value = models.BooleanField(null=True)
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question_id = models.ForeignKey(BooleanQuestion, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Boolean Answer: {self.value}"
    

class SingleChoiceAnswer(models.Model):
    """Modelo para respuestas tipo selección única."""
    value = models.CharField(max_length=255, blank=True, null=True)
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question_id = models.ForeignKey(OptionQuestion, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Single Choice Answer: {self.value}"

# class Answer(models.Model):
#     """Modelo para representar respuestas a preguntas específicas."""
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="answers"
#     )
#     # question = models.ForeignKey(
#     #     Question, on_delete=models.CASCADE, related_name="answers"
#     # )
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     response = GenericForeignKey('content_type', 'object_id')
    
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Answer from {self.user} to '{self.question}'"
