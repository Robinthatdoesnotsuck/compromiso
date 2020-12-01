from django.db import models

# Create your models here.
class Instituciones(models.Model):
    name = models.CharField(max_length = 200)
    area = models.CharField(max_length = 200, null=True)
    description = models.CharField(max_length = 400, null=True)
    image = models.ImageField(upload_to = 'profile_image')
    def __str__(self):
        return self.name

class Proyectos(models.Model):
    name = models.CharField(max_length = 200)
    institucion = models.ForeignKey(Instituciones, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name

class Actividades(models.Model):
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)
    text = models.CharField(max_length = 300,null=True)
    complete = models.BooleanField(null=True)
    horas = models.DecimalField(max_digits=3,decimal_places=0, null=True)
    inicio = models.CharField(max_length = 300, null=True)
    fin = models.CharField(max_length = 300, null=True)
    def __str__(self):
        return self.text
#from main.models import Actividades, Proyectos


class Estudiante(models.Model):
    name = models.CharField(max_length = 200)
    celular = models.CharField(max_length = 200, null = True)
    carrera = models.CharField(max_length = 200, null = True)
    horas = models.DecimalField(max_digits=3,decimal_places=0)
    actividades = models.ManyToManyField(Actividades, null = True)
    image = models.ImageField(upload_to = 'profile_image', blank = True)
    voluntariado = models.BooleanField(null = True)
    def __str__(self):
        return self.name
class Peticion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete = models.CASCADE, null = True)
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, null = True)
    aprobar = models.BooleanField(default = False)

class Compromiso(models.Model):
    name = models.CharField(max_length = 200)
    def __str__(self):
        return self.name