from django.http import JsonResponse, HttpResponse
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
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.templatetags.static import static
import re

from datetime import datetime

logger = logging.getLogger(__name__)

# View to check if the user is authenticated
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_auth(request):
    try:
        data = json.loads(request.body)  # Parse the JSON body
        username = data.get('username')  # Get the username from the request
        print("USERNAME: ", username)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not username:
        return JsonResponse({'error': 'Username is required'}, status=400)

    try:
        user = User.objects.get(username=username)  # Check if the user exists
        if user.is_authenticated:
            print("AUTHENTICATED")
            return JsonResponse({
                'is_authenticated': True,
                # 'is_staff': str(user.is_staff),  # Return 'true'/'false' as string
            })
        else:
            return JsonResponse({
                'is_authenticated': False
            })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


@api_view(['GET'])
@permission_classes([AllowAny])
def redirect_api(request):
    state = gen_state()
    logger.info("Redirect URI: %s", settings.REDIRECT_URI)
    go_to_api = (
        "https://api.intra.42.fr/oauth/authorize"
        f"?client_id={settings.UID}"
        f"&redirect_uri={settings.REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=public"
        f"&state={state}"
    )
    logger.info(f"Redirect URL: {go_to_api}")
    return redirect(go_to_api)



def gen_state():
	return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

class Callback42API(APIView):
    """ """

    permission_classes = [AllowAny]

    def get(self, request):

        code = request.GET.get('code')
        state = request.GET.get('state')
#        logger.info(f"Code: {code}, State: {state}")
        if not state or not code:
            raise AuthenticationFailed("Invalid authentication parameters")
        try:
            response = post42("/oauth/token", defaultParams(code, state))
            if response.status_code != 200:
                raise AuthenticationFailed("Bad response code while authentication")
            data = response.json()
            intra_token = data.get("access_token")
            res_front = saveUser(str(intra_token))
            data_res_front = json.loads(res_front.content)
            if res_front.status_code == 500:
                raise AuthenticationFailed(res_front.content['Error'])
            try:
                user = User.objects.get(username=data_res_front.get('username'))
            except User.DoesNotExist:
                raise Exception("No users found with the same username")
            except User.MultipleObjectsReturned:
                raise Exception("Multiple users found with the same username")
            user.is_active = True
            #####
            # refresh_intra_token = RefreshToken(intra_token)
            # BLOCKLIST.add(str(intra_token))  # Replace with your blocklist logic (e.g., saving to DB/Redis)
            # refresh_intra_token.blacklist()  # Use if you enabled Django REST Framework SimpleJWT's blacklist app
            #####
            django_login(request, user)
            # Test user authentication immediately after login
            if request.user.is_authenticated:
                print("User authenticated successfully:", request.user.username)
            else:
                print("User authentication failed")
            refresh_token = RefreshToken.for_user(user)
            formatResponse = data_res_front | {
                'refresh_token': str(refresh_token),
                'access': str(refresh_token.access_token),
                'intra_token': str(intra_token), 
                'id': user.id
                #USER ID!!!

             }
                        #####
            # refresh_intra_token = RefreshToken(intra_token)
            # BLOCKLIST.add(str(intra_token))  # Replace with your blocklist logic (e.g., saving to DB/Redis)
            # refresh_intra_token.blacklist()  # Use if you enabled Django REST Framework SimpleJWT's blacklist app
            #####
            return JsonResponse(formatResponse)
        except Exception as e:
            return JsonResponse({'Error': str(e)}, status=400)

def saveUser(token):
    try:
        user_res = get42('/v2/me', None, token)
        if user_res.status_code != 200:
            raise AuthenticationFailed("Bad response code while authentication")
        user_data = user_res.json()
        if not user_data.get('login'):
            raise AuthenticationFailed("Couldn't recognize the user")
        exist = User.objects.filter(username=user_data.get('login')).exists()
        if not exist:
            user = User(username=user_data.get('login'), is_42_staf=user_data.get('staff?'), email=user_data.get('email'), intra_id=user_data.get('id'))
            user.save()
        user_img = None # here the default
        if user_data['image']['link']:
            user_img = user_data['image']['link']
#        print("BEFORECOAL: ", user_img)
        coal_data = getCoalition(defaultUser(user_data.get('login'), user_data.get('staff?'), user_img), user_data.get('login'), token)
        # piscine / student / alumni
        return JsonResponse(coal_data)
    except Exception as e:
        return JsonResponse({"Error": str(e)}, status=500)

def defaultUser(login, is_staff, user_img):
    default =  {
        # 'status': 200,
        'username': login,
        'is_staff': is_staff,
        'user_img': user_img,
        'coalition': None,
        'color': "#00BABC",
        'coalition_img': None,
        'title': ""     
    }
    return default

def getCoalition(default, login, token):
    url_coal = "/v2/users/" + login + "/coalitions"
    coal_res = get42(url_coal, None, token)
    if coal_res.status_code != 200:
        return default
    coal_data = coal_res.json()
    if coal_data:
        default['coalition'] = coal_data[0]['name']
        default['color'] = coal_data[0]['color']
        default['coalition_img'] = coal_data[0]['cover_url']
    return default

def defaultParams(code, state):
    params = {
        'grant_type': 'authorization_code',
        'client_id': os.environ['UID'],
        'client_secret': os.environ['SECRET'],
        'code': code,
        'redirect_uri': os.environ['REDIRECT_URI'],
        'state': state
    }
    return params

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

# Example token blocklist (you may use a database or Redis for scalability)
BLOCKLIST = set()

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
def logout_view(request):
    # Get the refresh token from the request
      
    refresh_token = request.data.get('refresh_token')
    print("LOGOUT: ", request.data.get('refresh_token'))
    # 'intra_token'
    user = User.objects.get(username=request.data.get('username'))
    if refresh_token:
        try:
            # Blacklist the token
            token = RefreshToken(refresh_token)
            # BLOCKLIST.add(str(token))  # Replace with your blocklist logic (e.g., saving to DB/Redis)
            token.blacklist()  # Use if you enabled Django REST Framework SimpleJWT's blacklist app
        except Exception as e:
            return JsonResponse({'detail': 'Invalid token'}, status=400)
    
    # Log out the user from Django (clears session data)
    django_logout(request, user)
    
    # Clear the refresh token cookie
    response = JsonResponse({'detail': 'Successfully logged out'})
    response.delete_cookie('refresh_token')
    
    return response