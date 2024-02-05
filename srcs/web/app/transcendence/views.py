from django.shortcuts import render

# Create your views here.
def login(request):
	return render(request, 'views/login.html')

def signin(request):
	return render(request, 'views/signin.html')

def games(request):
	return render(request, 'views/games.html')

def pong(request, id_lobby):
	return render(request, 'views/games/pong.html', {'id_lobby': id_lobby})

def pew(request):
	return render(request, 'views/games/pew.html')