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
    intra_id = models.PositiveIntegerField(default=0)
#    gender = 
    name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_42_staf = models.BooleanField(default=False)
#    role = models.CharField(max_length=50,unique=False, blank=True)
#    coalition = JSONField(default=dict)
#    level = models.PositiveIntegerField(default=0)
#    age = models.PositiveIntegerField(default=0)
#    image_url = models.URLField(max_length=200, blank=True, null=True)

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
    type = 'text'
    max_chars = models.IntegerField(verbose_name='Maximo número de caracteres', default=1000)
    min_chars = models.IntegerField(verbose_name='Mínimo número de caracteres', default=1)
    text = models.CharField(max_length=300, verbose_name='Pregunta', blank=False, null=False)
    is_required = models.BooleanField(verbose_name='¿Respuesta requerida?', default=1)
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Text question'
        constraints = [
            models.UniqueConstraint(fields=['order', 'form_id_id'], name='unique_order_tq_per_form')
        ] 
        #garantiza que no se repitan numeros de pregunta dentro del form lo que evita que se repitan preguntas en el mismo formulario

    def __str__(self):
        return f"Pregunta {self.order}: {self.text}"

class BooleanQuestion(models.Model):
    order = models.IntegerField(verbose_name='pregunta número', blank=False, null=False)
    type = 'boolean'
    text = models.CharField(max_length=250, verbose_name='Pregunta', blank=False, null=False)
    is_required = models.BooleanField(verbose_name='¿Respuesta requerida?', default=1)
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Boolean question'

    def __str__(self):
        return f"Pregunta {self.order}: {self.text}"

class OptionQuestion(models.Model):
    order = models.IntegerField(verbose_name='pregunta número', blank=False, null=False)
    type = 'option'
    text = models.CharField(max_length=250, verbose_name='Pregunta', blank=False, null=False)
    options = models.JSONField(default=dict)
    is_required = models.BooleanField(verbose_name='¿Respuesta requerida?', default=1)
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)


    class Meta:
        db_table = 'Option question'

    def __str__(self):
        return f"Pregunta {self.order}: {self.text}"
    
class MultipleChoiceQuestion(models.Model):
    order = models.IntegerField(verbose_name='pregunta número', blank=False, null=False)
    type = 'multiple_choice'
    text = models.CharField(max_length=250, verbose_name='Pregunta', blank=False, null=False)
    options = models.JSONField(default=dict)
    is_required = models.BooleanField(verbose_name='¿Respuesta requerida?', default=1)
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Multiple Choice question'

    def __str__(self):
        return f"Pregunta {self.order}: {self.text}"
    
class NumberQuestion(models.Model):
    order = models.IntegerField(verbose_name='pregunta número', blank=False, null=False)
    type = 'number'
    text = models.CharField(max_length=250, verbose_name='Pregunta', blank=False, null=False)
    is_required = models.BooleanField(verbose_name='¿Respuesta requerida?', default=1)
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Number question'

    def __str__(self):
        return f"Pregunta {self.order}: {self.text}"
    
class EmailQuestion(models.Model):
    order = models.IntegerField(verbose_name='pregunta número', blank=False, null=False)
    type = 'email'
    text = models.CharField(max_length=320, verbose_name='Pregunta', blank=False, null=False)
    is_required = models.BooleanField(verbose_name='¿Respuesta requerida?', default=1)
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)

    class Meta:
        db_table = 'email_question' #Se recomienda sin espacios, porque!
        constraints = [
            models.UniqueConstraint(fields=['order', 'form_id_id'], name='unique_order_per_form')
        ] 
        #garantiza que no se repitan numeros de pregunta dentro del form lo que evita que se repitan preguntas en el mismo formulario

    def __str__(self):
        return f"Pregunta {self.order}: {self.text}"
    
class ScaleQuestion(models.Model):
    order = models.IntegerField(verbose_name='pregunta número', blank=False, null=False)
    type = 'scale'
    text = models.CharField(max_length=320, verbose_name='Pregunta', blank=False, null=False)
    min_value = models.IntegerField(verbose_name='Valor mínimo', default=1)
    max_value = models.IntegerField(verbose_name='Valor máximo', default=5)
    is_required = models.BooleanField(verbose_name='¿Respuesta requerida?', default=1)
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Scale question'
    
    def __str__(self):
        return f"Pregunta {self.order}: {self.text}"
    
class DateQuestion(models.Model):
    order = models.IntegerField(verbose_name='pregunta número', blank=False, null=False)
    type = 'date'
    text = models.CharField(max_length=320, verbose_name='Pregunta', blank=False, null=False)
    is_required = models.BooleanField(verbose_name='¿Respuesta requerida?', default=1)
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Date question'
    
    def __str__(self):
        return f"Pregunta {self.order}: {self.text}"
    
class URLQuestion(models.Model):
    order = models.IntegerField(verbose_name='pregunta número', blank=False, null=False)
    type = 'url'
    text = models.CharField(max_length=320, verbose_name='Pregunta', blank=False, null=False)
    is_required = models.BooleanField(verbose_name='¿Respuesta requerida?', default=1)
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'URL question'
    
    def __str__(self):
        return f"Pregunta {self.order}: {self.text}"

class FileQuestion(models.Model):
    order = models.IntegerField(verbose_name='pregunta número', blank=False, null=False)
    type = 'file'
    text = models.CharField(max_length=320, verbose_name='Pregunta', blank=False, null=False)
    is_required = models.BooleanField(verbose_name='¿Respuesta requerida?', default=1)
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'File question'
        
    def __str__(self):
        return f"Pregunta {self.order}: {self.text}"

class   SentForm(models.Model):
    form_id = models.ForeignKey(Form, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    sended = models.DateTimeField(verbose_name='sended')
    answered = models.BooleanField(verbose_name='answered', default=False)

    class Meta:
        db_table = 'SentForm'
        
    def __str__(self):
        return f" {self.form_id.name } sent to {self.user_id.email}"


# Modelos de respuesta

class Answer(models.Model):
    """Modelo para representar respuestas a preguntas específicas."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="answers")
    sent_form = models.ForeignKey(SentForm, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=False)
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
    
class MultipleChoiceAnswer(models.Model):
    """Modelo para respuestas tipo Multiple Choice."""
    value = models.JSONField(default=dict)
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question_id = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f"Multiple Choice Answer: {self.value}"
    
class NumberAnswer(models.Model):
    """Modelo para respuestas tipo Number."""
    value = models.IntegerField(default=0)
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question_id = models.ForeignKey(NumberQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f"Opinion Scale Answer: {self.value}"
    
class EmailAnswer(models.Model):
    """Modelo para respuestas tipo selección única."""
    value = models.EmailField(max_length=320, blank=True, null=True)
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='email_answers')
    question_id = models.ForeignKey(EmailQuestion, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Email Answer: {self.value} for Question ID {self.question_id}"

class ScaleAnswer(models.Model):
	"""Modelo para respuestas tipo escala."""
	value = models.IntegerField()
	answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
	question_id = models.ForeignKey(ScaleQuestion, on_delete=models.CASCADE)
	
	def clean(self):
		"""Valida que el valor esté dentro del rango de la pregunta."""
		if not (self.question_id.min_value <= self.value <= self.question_id.max_value):
			raise ValidationError(
				f"El valor debe estar entre {self.question_id.min_value} y {self.question_id.max_value}."
			)

	def __str__(self):
		return f"Scale Answer: {self.value}"

class DateAnswer(models.Model):
    """Modelo para respuestas tipo fecha."""
    value = models.DateField()
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question_id = models.ForeignKey(DateQuestion, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Date Answer: {self.value}"
    
class URLAnswer(models.Model):
    """Modelo para respuestas tipo URL."""
    value = models.URLField()
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question_id = models.ForeignKey(URLQuestion, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"URL Answer: {self.value}"
    
class FileAnswer(models.Model):
    """Modelo para respuestas tipo archivo."""
    value = models.FileField(upload_to='uploads/')
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question_id = models.ForeignKey(FileQuestion, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"File Answer: {self.value}"

#     def __str__(self):
#         return f"Answer from {self.user} to '{self.question}'"

class Campus(models.Model):
    id_42 = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name

class Cursus(models.Model):
    id_42 = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name
