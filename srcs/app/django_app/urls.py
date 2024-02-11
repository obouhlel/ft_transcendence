from django.contrib import admin
from django.urls import path
from transcendence import views

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', views.index, name='index'),
	path('sections/<str:section>/', views.section, name='section'),
	path('home/', views.home, name='home'),
	path('login/', views.login_user, name='login'),
	path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
	path('profile/', views.profile, name='profile'),
	path('edit_profile/', views.edit_profile, name='edit_profile'),
	path('games/', views.games, name='games'),
	path('game/<int:game_id>/', views.game, name='game'),
    path('pong/', views.pong, name='pong'),
	path('shooter/', views.shooter, name='shooter'),
]
