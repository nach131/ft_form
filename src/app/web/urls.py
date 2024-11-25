from django.urls import path
from .views import login
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

from .views.todo import (
    home, err, Cheat,
)

urlpatterns = [
    path("", home, name="home"),
    path("cheat/", Cheat, name="home"),
    path('err/', err, name='err'),
    path('login/', login.redirect_api, name="redirect_api"),
]
