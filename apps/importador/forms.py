from django import forms
from .models import Importacion

class ImportadorForm(forms.ModelForm):
    class Meta:
        model = Importacion
        fields = ('archivo',)

class ProcesarImportacionForm(forms.ModelForm):
    procesado = forms.BooleanField(label='Procesar alumnos')
    class Meta:
        model = Importacion
        fields = ('procesado',)