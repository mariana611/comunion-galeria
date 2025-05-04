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
from django.shortcuts import render
from .models import Foto
# Vista para acceder a la galería


def galeria(request):
    fotos = Foto.objects.all()
    return render(request, 'galeria.html', {'fotos': fotos})


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
    if request.method == 'POST' and request.FILES['imagen']:
        imagen = request.FILES['imagen']
        # Subir la imagen a Cloudinary
        upload_result = cloudinary.uploader.upload(imagen)
        # Obtener la URL de la imagen
        foto_url = upload_result['url']

        # Guardar la foto en la base de datos
        foto = Foto(imagen=imagen, url_imagen=foto_url)
        foto.save()

        return redirect('galeria')
    else:
        form = FotoForm()

    return render(request, 'subir_foto.html', {'form': form})

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

# Vista para borrar una foto
@csrf_protect
def borrar_foto(request, foto_id):
    if request.method == 'POST':
        clave_ingresada = request.POST.get("clave")
        if clave_ingresada == settings.CLAVE_BORRAR_FOTO:
            foto = get_object_or_404(Foto, id=foto_id)

            # Aquí eliminarás el archivo físico de la imagen en el almacenamiento local
            if foto.imagen:
                # Asegúrate de que el archivo existe y eliminarlo
                try:
                    # Obtén la ruta absoluta del archivo
                    archivo_path = foto.imagen.path
                    if os.path.exists(archivo_path):
                        os.remove(archivo_path)
                except Exception as e:
                    print(f"Error al intentar eliminar la imagen: {e}")

            # Elimina la entrada en la base de datos
            foto.delete()
            return redirect('galeria')
        else:
            error = "Clave incorrecta. No tienes permiso para borrar esta foto."
            return render(request, "fotos/galeria.html", {"error": error})

    return render(request, "fotos/galeria.html")