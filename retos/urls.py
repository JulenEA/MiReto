from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "retos"

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('crear-reto', views.crear_reto, name='add-reto'),
    path('anadir-progreso', views.add_progreso, name='add-progreso'),
    path('anadir-progreso/<int:reto_id>', views.add_progreso, name='add-progreso-id'),
    path('retos/<str:nombre_usuario>', views.reto, name='reto'),
    #path('pruebas', views.pruebas, name='pruebas'),
    path('error', views.error, name='error'),
]