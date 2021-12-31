from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "usuarios"

urlpatterns = [

    path('login', auth_views.LoginView.as_view(template_name="usuarios/login.html"), name="login"),
    path('editar-usuario', views.editar_usuario, name='editar_usuario'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('registro', views.registro, name="registro")
]