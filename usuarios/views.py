from django.contrib.auth import authenticate
from django.shortcuts import redirect, render

from django.shortcuts import render

from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm  

from django.contrib.auth import authenticate, login


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            #authenticate user then login
            nuevo_usuario = authenticate(username=username, password=password)
            login(request, nuevo_usuario)


            return redirect('retos:reto', nombre_usuario=nuevo_usuario.username)

    else:
        form = UserCreationForm()
    
    return render(
        request,
        "usuarios/registro.html",
        {"form": form}
    )

def editar_usuario(request):
    return HttpResponse("Edit user")


def logout(request):
    return HttpResponse("Logout screen")
