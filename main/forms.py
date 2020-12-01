from django import forms
from .models import *
class CrearNuevaActividad(forms.Form):
    name = forms.CharField(label = "Name",max_length = 200)
    check = forms.BooleanField(required = False) 

class CrearNuevoProyecto(forms.Form):
    name = forms.CharField(label = "Name",max_length = 200)

class InstitucionForm(forms.ModelForm):
    area = forms.CharField()
    description = forms.CharField()
    class Meta:
        model = Instituciones
        fields = ['area','description']

class EstudianteForm(forms.ModelForm):
    celular = forms.CharField()
    carrera = forms.CharField()
    
    class Meta:
        model = Estudiante
        fields = ['celular', 'carrera']