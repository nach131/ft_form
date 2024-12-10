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

def Login(request):
    return render(request, "login.html")

def CallbackFront(request):
    return render(request, 'calback42.html')

def StudentHome(request):
    return render(request, 'studenthome.html')

def StaffHome(request):
    return render(request, 'staffhome.html')

def answer_form(request):
	return render(request,'questionaire.html')