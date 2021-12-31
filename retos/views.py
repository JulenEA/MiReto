from django.shortcuts import redirect, render
from .models import Progreso, Reto
from .objetos import RetoObject
from .forms import CrearRetoForm, AddProgresoForm
from datetime import date

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required



def inicio(request):

    mensaje = ""
    if request.method == "GET" and "busqueda" in request.GET:
        nombre_usuario = request.GET.get("busqueda", "").lower()
        try:
            User.objects.get(username=nombre_usuario)
            return redirect('retos:reto', nombre_usuario=nombre_usuario)
        except User.DoesNotExist:
            mensaje = "Usuario no encontrado."


    return render(
        request,
        "retos/inicio.html",
        {
            "mensaje": mensaje
        }
    )


def reto(request, nombre_usuario):
    
    try:
        user = User.objects.get(username=nombre_usuario)
    except User.DoesNotExist:
        return render(
            request,
            "retos/usuario_no_existe.html"
        )

    retos_qs = Reto.objects.filter(usuario=user)

    retos = []
    for reto in retos_qs:
        retos.append(RetoObject(reto))
    
    es_propio = False
    if nombre_usuario == request.user.username:
        es_propio = True

    return render(
        request,
        "retos/reto.html",
        {
            "retos": retos,
            "es_propio": es_propio
        }
    )

@login_required
def crear_reto(request):
    
    if request.method == "POST":
        form = CrearRetoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            objetivo = form.cleaned_data["objetivo"]
            unidades = form.cleaned_data["unidad"]
            fecha_inicio = form.cleaned_data["fecha_inicio"]
            fecha_fin = form.cleaned_data["fecha_fin"]

            reto = Reto()
            reto.nombre = nombre
            reto.objetivo = objetivo
            reto.unidad = unidades
            reto.fecha_inicio = fecha_inicio
            reto.fecha_fin = fecha_fin
            reto.usuario = request.user

            reto.save()

            return redirect("retos:reto", nombre_usuario = request.user.username)
    else:
        form = CrearRetoForm()


    return render(
        request,
        "retos/crear_reto.html",
        {
            "form": form
        }
    )

@login_required
def add_progreso(request, reto_id=None):

    if request.method == "POST":
        form = AddProgresoForm(request.POST)
        form.fields["reto"].queryset = Reto.objects.filter(usuario=request.user)
        if form.is_valid():
            cantidad = form.cleaned_data["cantidad"]
            reto = form.cleaned_data["reto"]

            if reto.usuario == request.user:
                progreso = Progreso()
                progreso.cantidad = cantidad
                progreso.reto = reto
                progreso.save()

            return redirect("retos:reto", nombre_usuario = request.user.username)
    
    else:
        form = AddProgresoForm()
        form.fields["reto"].queryset = Reto.objects.filter(usuario=request.user, fecha_inicio__lte=date.today(), fecha_fin__gte=date.today())
    
    if reto_id is not None:
        form.fields["reto"].initial = reto_id

    return render(
        request,
        "retos/add_progreso.html",
        {
            "form": form
        }
    )

def error(request):
    return render(
        request,
        "error.html",
    )


def pruebas(request):
    return render(
        request,
        "pruebas.html",
    )