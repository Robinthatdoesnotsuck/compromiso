from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>", views.index, name = "index"),
    path("", views.home, name = "home"),
    path("proyectoser/<int:id>", views.proyectoestudent, name = "proyectoestudent"),
    path("actividad/<int:id>", views.actividadstudent, name = "actividad"),
    path("proyectos", views.proyectos, name = "proyectos"),
    path("estudiante", views.estudiante, name ="estudiante"),
    path("institucion", views.institucion, name = "institucion"),
    path("estudiantescomp", views.estudiantescomp, name = "estudiantescomp"),
    path("institucionpage", views.institucionpage ,name ="institucionpage"),
    path("general", views.general, name = "general")
]