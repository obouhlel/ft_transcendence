from django.utils import timezone
from django.contrib.auth import login as django_login
from transcendence.models import CustomUser
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
        return user
    else:
        return None

def authenticate_user(request, user):
    django_login(request, user)
    user.status = 'online'
    user.save()
    return redirect('/')

def redirect_with_message(url, message):
    url += '?' + urlencode({'message': message})
    return redirect(url)

@require_http_methods(['GET'])
def login_42(request):
    code = request.GET.get('code')
    if code:
        access_token, token_type = get_access_token(code, request)
        if access_token and token_type:
            user_data = get_user_data(access_token, token_type)
            if user_data:
                if CustomUser.objects.filter(token=access_token).exists():
                    user = CustomUser.objects.get(username=user_data['login'])
                    return authenticate_user(request, user)
                else:
                    if CustomUser.objects.filter(username=user_data['login']).exists():
                        return redirect_with_message('/#400', 'This username is already in use.')
                    if CustomUser.objects.filter(email=user_data['email']).exists():
                        return redirect_with_message('/#400', 'This email is already in use.')
                    user = create_user(user_data, access_token)
                    if user:
                        return authenticate_user(request, user)
                    else:
                        return redirect_with_message('/#400', 'Unable to create user.')
            else:
                return redirect_with_message('/#400', 'Unable to retrieve user data.')
        else:
            return redirect_with_message('/#400', 'Unable to retrieve access token.')
    else:
        return redirect_with_message('/#400', 'Invalid code.')