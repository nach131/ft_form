from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import json

from django.views import View
import os


def err(request):
    return render(request, '404.html')


def home(request):
    return render(request, "home.html")


def Cheat(request):
    return render(request, "cheat.html")
