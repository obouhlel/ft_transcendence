from django.contrib import admin
from django.urls import path, include
from transcendence import views

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', views.index, name='index'),

	# VIEWS (SHHOW PAGES)
	path('sections/<str:section>/', views.section, name='section'),

	# METHODS POST ET GET (API)
	path('api/', include("transcendence.api")),
]
