from django.urls import path

from .views.todo import (
    home, err, Cheat,
)

urlpatterns = [
    path("", home, name="home"),
    path("cheat/", Cheat, name="home"),

    path('err/', err, name='err'),

]
