from django import forms
from .models import Foto, Comentario

from django.core.exceptions import ValidationError
from .models import Foto


class FotoForm(forms.ModelForm):
    class Meta:
        model = Foto
        fields = ['imagen', 'categoria']

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')

        # Verificar si ya existe una foto con el mismo hash_imagen
        hash_imagen = Foto.generate_hash(imagen)
        if Foto.objects.filter(hash_imagen=hash_imagen).exists():
            raise ValidationError("Ya existe una foto con este archivo. Por favor, usa otro archivo.")

        return imagen


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
