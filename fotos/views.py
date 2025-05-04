from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Foto, Comentario
from .forms import FotoForm
from django.http import FileResponse
import os
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
# Vista para acceder a la galería
def galeria(request):
    if not request.session.get("acceso_permitido"):  # Verifica si el usuario tiene acceso
        return redirect("acceso")

    fotos = Foto.objects.all().order_by('-fecha_subida')  # Muestra las fotos más recientes primero
    return render(request, 'fotos/galeria.html', {'fotos': fotos})

#def galeria(request):
    #fotos = Foto.objects.all()
    #return render(request, 'fotos/galeria.html', {'fotos': fotos})
# Vista para comentar en una foto




# Vista de acceso con clave
def acceso(request):
    if request.method == "POST":
        clave_ingresada = request.POST.get("clave")
        if clave_ingresada == settings.CLAVE_DE_ACCESO:
            request.session["acceso_permitido"] = True  # Guardamos la sesión
            return redirect("galeria")  # Redirige a la galería de fotos
        else:
            error = "Clave incorrecta. Inténtalo de nuevo."
            return render(request, "fotos/acceso.html", {"error": error})

    return render(request, "fotos/acceso.html")


def subir_foto(request):
    if request.method == 'POST':
        form = FotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('galeria')  # Redirigir a la galería después de subir la foto
    else:
        form = FotoForm()

    return render(request, 'fotos/subir_foto.html', {'form': form})

@csrf_protect
def comentar(request, foto_id):
    if not request.session.get("acceso_permitido"):  # Verifica si el usuario tiene acceso
        return redirect("acceso")

    foto = get_object_or_404(Foto, id=foto_id)

    if request.method == "POST":
        texto = request.POST.get("comentario")
        if texto:
            Comentario.objects.create(foto=foto, texto=texto)

    return redirect("galeria")


# Vista para borrar una foto
@csrf_protect
def borrar_foto(request, foto_id):
    if request.method == 'POST':
        clave_ingresada = request.POST.get("clave")
        if clave_ingresada == settings.CLAVE_BORRAR_FOTO:
            foto = get_object_or_404(Foto, id=foto_id)
            foto.delete()
            return redirect('galeria')
        else:
            error = "Clave incorrecta. No tienes permiso para borrar esta foto."
            return render(request, "fotos/galeria.html", {"error": error})

    return render(request, "fotos/galeria.html")  # Si no es POST, simplemente muestra la galería
