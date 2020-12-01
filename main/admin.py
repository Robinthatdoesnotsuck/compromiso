from django.contrib import admin
from .models import Proyectos,Actividades, Instituciones, Estudiante,Compromiso
# Register your models here.

admin.site.register(Proyectos)
admin.site.register(Actividades)
admin.site.register(Instituciones)
admin.site.register(Estudiante)
admin.site.register(Compromiso)