from django.contrib import admin
from django.urls import path
from transcendence import views

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', views.login_user, name='login'),
	path('login/', views.login_user, name='login'),
	path('signin/', views.signin_user, name='signin'),
    path('logout/', views.logout_user, name='logout'),
	path('games/', views.games),
	path('game/', views.game),
    path('pong/', views.pong),
	path('shooter/', views.shooter),
]
