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

def create_user(user_data, access_token):
    username = user_data['login']
    email = user_data['email']
    firstname = user_data['usual_first_name']
    if not firstname:
        firstname = user_data['first_name']
    lastname = user_data['last_name']
    avatar_url = user_data.get('image', {}).get('link')
    response = requests.get(avatar_url)
    if response.status_code == 200:
        avatar_file = ContentFile(response.content)
        avatar_file.name = username + '.jpg'
        user = CustomUser.objects.create(
            username=username,
            email=email,
            first_name=firstname,
            last_name=lastname,
            avatar=avatar_file,
            token=access_token,
            date_joined=timezone.now()
        )
        # delete this if many games or many users
        for game in Game.objects.all():
            Stat_User_by_Game.objects.create(user=user, game=game)
        return user
    else:
        return None

def authenticate_user(request, user):
    django_login(request, user)
    user.status = 'Online'
    user.save()
    return redirect('/')

def redirect_with_message(url, message):
    url += '?' + urlencode({'message': message})
    return redirect(url)

@require_http_methods(['GET'])
def login_42(request):
    code = request.GET.get('code')
    if not code:
        return redirect_with_message('/#400', 'No code provided.')
    
    access_token, token_type = get_access_token(code, request)
    if  not access_token or not token_type:
        return redirect_with_message('/#400', 'Unable to retrieve access token.')
    user_data = get_user_data(access_token, token_type)
    if not user_data:
        return redirect_with_message('/#400', 'Unable to retrieve user data.')
    if CustomUser.objects.filter(token=access_token).exists():
        user = CustomUser.objects.get(username=user_data['login'])
        return authenticate_user(request, user)
    if CustomUser.objects.filter(username=user_data['login']).exists():
        return redirect_with_message('/#400', 'This username is already in use.')
    if CustomUser.objects.filter(email=user_data['email']).exists():
        return redirect_with_message('/#400', 'This email is already in use.')
    user = create_user(user_data, access_token)
    if not user:
        return redirect_with_message('/#400', 'Unable to create user.')
    return authenticate_user(request, user)