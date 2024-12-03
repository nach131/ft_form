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
    is_active = models.BooleanField(default=True)
    is_cancel = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_42_staf = models.BooleanField(default=False)
    role = models.CharField(max_length=50,unique=False, blank=True)
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



# Modelos de respuesta

class CharFieldAnswer(models.Model):
    """Modelo para respuestas tipo texto."""
    value = models.CharField(
        max_length=255, blank=True, null=True,
        validators=[MinLengthValidator(3)]
    )

    def __str__(self):
        return f"CharField Answer: {self.value}"

class BooleanAswer(models.Model):
    """Modelo para respuestas tipo booleano."""
    value = models.BooleanField(null=True)
    
    def __str__(self):
        return f"Boolean Answer: {self.value}"
    

class SingleChoiceAnswer(models.Model):
    """Modelo para respuestas tipo selección única."""
    value = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Single Choice Answer: {self.value}"

# class Answer(models.Model):
#     """Modelo para representar respuestas a preguntas específicas."""
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="answers"
#     )
#     question = models.ForeignKey(
#         Question, on_delete=models.CASCADE, related_name="answers"
#     )
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     response = GenericForeignKey('content_type', 'object_id')
    
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Answer from {self.user} to '{self.question}'"

