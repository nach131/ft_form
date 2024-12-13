from django.urls import path
from .views import login
from .views.login import Callback42API
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

from .views.todo import (
    home, err, Cheat, Login, CallbackFront, StudentHome, StaffHome, answer_form,
)

urlpatterns = [
    #path("", home, name="home"),
    path("cheat/", Cheat, name="home"),
    path('err/', err, name='err'),
    path("", Login, name='login'),
    path('login/redirect', login.redirect_api, name="redirect_api"),
    path('login/callback', CallbackFront, name='front_callback'),
    path('login/handleCallback', Callback42API.as_view(), name="callback"),
    path('logout', login.logout_view, name="logout_view"),
    path('studentHome', StudentHome, name='studenthome'),
    path('staffHome', StaffHome, name='staffHome'),
	path('answerForm', answer_form, name='answer_form'),
    path('check-auth', login.check_auth, name="check_auth"),
  #  path('login/callback', Callback42API.as_view(), name="callback"),
]
