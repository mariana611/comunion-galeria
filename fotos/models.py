from django.db import models
import hashlib
from cloudinary.models import CloudinaryField
# Modelo para las fotos
class Foto(models.Model):
    CATEGORIAS = [
        ('iglesia', 'Iglesia'),
        ('celebracion', 'Celebración'),
        ('otros', 'Otros'),
    ]
    imagen = CloudinaryField('image')
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    hash_imagen = models.CharField(max_length=255, null=True, blank=True)  # Aquí haces que sea opcional


    def save(self, *args, **kwargs):
        # Calculamos el hash de la imagen antes de guardar
        if not self.hash_imagen and self.imagen:
            self.hash_imagen = self.generate_hash(self.imagen)
        super().save(*args, **kwargs)

    def generate_hash(self, image):
        """
        Genera un hash para una imagen basado en su contenido.
        """
        image_file = image.file
        image_file.seek(0)  # Asegurarse de leer desde el principio del archivo
        file_hash = hashlib.sha256()
        while chunk := image_file.read(4096):  # Leer en trozos
            file_hash.update(chunk)
        return file_hash.hexdigest()

    def __str__(self):
        return f"Foto {self.id} - {self.get_categoria_display()}"

# Modelo para los comentarios
class Comentario(models.Model):
    foto = models.ForeignKey(Foto, on_delete=models.CASCADE, related_name="comentarios")
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario en {self.foto.id} el {self.fecha.strftime('%Y-%m-%d %H:%M')}"
