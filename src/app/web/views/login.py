from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt
# from django.forms.models import model_to_dict
# from django.core.files.base import ContentFile
# from PIL import Image
from pathlib import Path
from core.models import User, UserManager
import logging
import json
import os
import random
import string
import requests

from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
import re

from datetime import datetime

logger = logging.getLogger(__name__)

@api_view(['GET'])
def redirect_api(request):
    state = gen_state()
    go_to_api = (
        "https://api.intra.42.fr/oauth/authorize"
        f"?client_id={settings.UID}"
        f"&redirect_uri={settings.REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=public"
        f"&state={state}"
    )
    return redirect(go_to_api)

def gen_state():
	return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

class Callback42API(APIView):
    def get(self, request):
#        try:
#       body = json.loads(request.body.decode('utf-8'))
        code = request.GET.get('code')
        state = request.GET.get('state')
        if not state or not code:
            raise AuthenticationFailed("Invalid authentication parameters")
        # response = {'response': 'POST'}
        params = {
            'grant_type': 'authorization_code',
            'client_id': os.environ['UID'],
            'client_secret': os.environ['SECRET'],
            'code': code,
            'redirect_uri': os.environ['REDIRECT_URI'],
            'state': state
        }
        try:
            response = post42("/oauth/token", params)
            if response.status_code != 200:
                raise AuthenticationFailed("Bad response code while authentication")
            data = response.json()
            #return JsonResponse(data)
            intra_token = data.get("access_token")
            user = saveUser(str(intra_token))
            #return JsonResponse({'Username: ': user.name})
            if (user == AnonymousUser):
                raise AuthenticationFailed("Couldn't find or save the user")
            django_login(request, user)
            refresh_token = RefreshToken.for_user(user)
            # logger.info(refresh_token["exp"])
            # logger.info(refresh_token.access_token["exp"])
            # logger.info(datetime.now().timestamp())
            formatResponse = {
                'refresh_token': str(refresh_token),
                'access': str(refresh_token.access_token),
                'refresh_exp': str(refresh_token["exp"] - datetime.now().timestamp()),
                'token_exp': str(refresh_token.access_token["exp"] - datetime.now().timestamp()),
                'username': user.name,
            }
            
            return JsonResponse(formatResponse)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def saveUser(token):
    try:
        res = get42('/v2/me', None, token)
        if res.status_code != 200:
            return AnonymousUser()
        data = res.json()
        exist = User.objects.filter(name=data.get('login')).exists()
        if exist:
            return User.objects.get(name=data.get('login'))
        url_coal = "/v2/users/" + data.get('login') + "/coalitions"
        coal_res = get42(url_coal, None, token)
        coal_data = coal_res.json()
        # HERE EXTRACT DATA ABOUT COALITION
        user = User(name=data.get('login'), is_42_staf=data.get('staff?'), 
                    email=data.get('email'))
        # add coalition, piscine / student / alumni, image
        user.save()
        return user
    except Exception as e:
        return AnonymousUser()



def post42(url, vars):
    url = "https://api.intra.42.fr" + url
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=vars)
    return response

def get42(url, vars, auth):
    url = "https://api.intra.42.fr" + url
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + auth
    }
    response = requests.request("GET", url, headers=headers)
    return response