from django.utils import timezone
from django.contrib.auth import login as django_login
from transcendence.models import CustomUser, Game, Stat_User_by_Game
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.core.files.base import ContentFile
from urllib.parse import urlencode
import requests

def get_access_token(code, request):
    token_url = 'https://api.intra.42.fr/oauth/token'
    client_id = settings.API_42_UID
    secret_key = settings.API_42_SECRET
    redirect_uri = settings.API_42_REDIRECT_URI.replace('$HOST', request.get_host())
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': secret_key,
        'code': code,
        'redirect_uri': redirect_uri,
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json()['access_token'], response.json()['token_type']
    else:
        return None, None

def get_user_data(access_token, token_type):
    user_url = 'https://api.intra.42.fr/v2/me'
    headers = {
        'Authorization': token_type + ' ' + access_token,
    }
    response = requests.get(user_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def authenticate_user(request, user):
    if user.status == 'Online':
        return redirect_with_message('/#400', 'User is already logged in.')
    django_login(request, user)
    return redirect('/')

def redirect_with_message(url, message):
    url += '?' + urlencode({'message': message})
    return redirect(url)

def save_user_data(user_data, access_token):
    data = {
        'username': user_data['login'],
        'email': user_data['email'],
        'first_name': user_data['usual_first_name'] if user_data['usual_first_name'] else user_data['first_name'],
        'last_name': user_data['last_name'],
        'token': access_token,
    }
    return data

@require_http_methods(['GET'])
def login_42(request):
    code = request.GET.get('code')
    if not code:
        return redirect_with_message('/#400', 'No code provided.')
    access_token, token_type = get_access_token(code, request)
    if not access_token or not token_type:
        return redirect_with_message('/#400', 'Unable to retrieve access token.')
    user_data = get_user_data(access_token, token_type)
    if not user_data:
        return redirect_with_message('/#400', 'Unable to retrieve user data.')
    if CustomUser.objects.filter(token=access_token).exists():
        user = CustomUser.objects.get(token=access_token)
        return authenticate_user(request, user)
    data = save_user_data(user_data, access_token)
    request.session['data'] = data
    return redirect('/#register-42')