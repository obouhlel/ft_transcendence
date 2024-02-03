from django.shortcuts import render

# Create your views here.
def login(request):
	return render(request, 'views/login.html')

def signin(request):
	return render(request, 'views/signin.html')

def games(request):
	return render(request, 'views/games.html')

def pong(request):
	return render(request, 'views/games/pong.html')

def pew(request):
	return render(request, 'views/games/pew.html')