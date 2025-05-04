from django import forms
from .models import Foto, Comentario

from django.core.exceptions import ValidationError
from .models import Foto


class FotoForm(forms.ModelForm):
    class Meta:
        model = Foto
        fields = ['imagen', 'categoria']




class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
