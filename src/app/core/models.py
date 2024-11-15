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
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

import secrets


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
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_cancel = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
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
