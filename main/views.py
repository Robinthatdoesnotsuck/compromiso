from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from .models import Proyectos, Actividades, Instituciones, Estudiante, Compromiso, Peticion
from .forms import CrearNuevoProyecto,CrearNuevaActividad, EstudianteForm, InstitucionForm
from django.contrib.auth.models import User
from register.views import register

# Create your views here.
def proyectoestudent(response, id):
    institucion = Instituciones.objects.get(id = id)
    estudiante= Estudiante.objects.get(name = response.user.username)
    group = str(response.user.groups.filter(name = "estudiante")[0])
    if response.method == "POST":
        if response.POST.get("solicitar"):
            for proyect in institucion.proyectos_set.all():
                print(response.POST.get("c" + str(proyect.id)) == "clicked")
                if response.POST.get("c" + str(proyect.id)) == "clicked":
                    print("pedir")
                    nuevaPeticion = Peticion(estudiante = estudiante, proyecto = proyect, aprobar = False)
                    nuevaPeticion.save()
                else:
                    print("esta no se pidio")
               
    return render(response, "main/proyectossearch.html", {"institucion": institucion, "estudiante":estudiante, "group": group})
def actividadstudent(response, id):
    proyecto = Proyectos.objects.get(id = id)
    estudiante= Estudiante.objects.get(name = response.user.username)
    group = str(response.user.groups.filter(name = "estudiante")[0])
    return render(response, "main/activities.html", {"proyectos": proyecto,"group": group, "estudiante": estudiante})

def estudianteinstituto(response, id):
    estudiante = Estudiante.objects.get(id = id)
    institucion = Instituciones.objects.get( name = response.user.username)
    group = str(response.user.groups.filter(name = "instituto")[0])

def index(response, id): 
    proyectos = Proyectos.objects.get(id = id)
    if response.method == "POST":
        print(response.POST)
        if response.POST.get("save"):
            for item in proyectos.actividades_set.all():
                if response.POST.get("c" + str(item.id)) == "clicked":
                    estudiantes_con_completados = Estudiante.objects.filter(actividades = item.id)
                    #print(estudiantes_con_completados)
                    for estu in estudiantes_con_completados:
                        estu.horas = estu.horas + item.horas
                        estu.save()
                        print(estu.horas)
                    #estudiantes_con_completados.horas = estudiantes_con_completados.horas + item.horas
                    #estudiantes_con_completados.save()
                    item.complete = True
                else:
                    item.complete = False
                item.save()
        elif response.POST.get("aprobar"):
            for peticion in proyectos.peticion_set.all():
                if response.POST.get("p" + str(peticion.id)):
                    peticion.aprobar= True
                    peticion.save()
                else:
                    print("No aprobada")
        elif response.POST.get("nuevaActividad"): 
            txt = response.POST.get("text")
            iniciod = response.POST.get("inicio")
            find = response.POST.get("fin")
            horasd = response.POST.get("horas")
            if len(txt) > 2:
                proyectos.actividades_set.create(text = txt, complete = False, horas = horasd, fin = find, inicio = iniciod)
            else:
                print("Invalid input")
    group = str(response.user.groups.filter(name = "instituto")[0])
    institucion = Instituciones.objects.get( name = response.user.username)
    return render(response, "main/activities.html", {"proyectos": proyectos,"group": group, "institucion": institucion})

def proyectos(response):
    institucion = Instituciones.objects.get( name = response.user.username)
    group = str(response.user.groups.filter(name = "instituto")[0])
    if response.method == "POST":
        if response.POST.get("nuevoProyecto"):
            nme = response.POST.get("text")
            if len(nme) > 2:
                institucion.proyectos_set.create(name = nme)
            else:
                print("Invalid input")
            return render(response, "main/general.html",{"institucion": institucion, "group": group})
    else:
        form = CrearNuevoProyecto()
        return render(response, "main/general.html",{"institucion": institucion,"group": group})

        #return render(response, "main/dashboard_student.html",{"estudiante": estudiante})
def general(response):
    if response.user.groups.filter(name = "instituto").exists():
        institucion = Instituciones.objects.get( name = response.user.username)
        return HttpResponseRedirect("/institucion",{"institucion": institucion})
    elif response.user.groups.filter(name = "estudiante").exists():
        estudiante= Estudiante.objects.get(name = response.user.username)
        return HttpResponseRedirect("/estudiante", {"estudiante":estudiante})
    elif response.user.groups.filter(name = "compromiso").exists():
        compromiso = Compromiso.objects.get(name = response.user.username)
        return HttpResponseRedirect("/register", {"compromiso":compromiso})

def institucion(request):
    institucion = Instituciones.objects.get( name = request.user.username)
    group = str(request.user.groups.filter(name = "instituto")[0])
    print(group)
    if request.method == "POST":
        form = InstitucionForm(request.POST,request.FILES, instance=institucion)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/institucion",{"institucion": institucion})
    else:
        form = InstitucionForm()
    return render(request, "main/instituto.html", {"institucion": institucion, "form": form, "group": group})
def home(response):
    return render(response, "main/home.html", {})

def login(response):
    return render(response, "registration/login.html", {})

def crud(response):
    if response.method == "POST":
        form = CrearNuevoProyecto(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            p = Proyectos(name = n)
            p.save()

        return HttpResponseRedirect("/%i" %p.id)

    else:
        form = CrearNuevoProyecto()
    return render(response, "main/general.html", {"form":form})

def estudiante(request):
    estudiante= Estudiante.objects.get(name = request.user.username)
    actividad_completadas = estudiante.actividades.filter(complete = True)
    actividad_incompletadas = estudiante.actividades.filter(complete = False)
    group = str(request.user.groups.filter(name = "estudiante")[0])
    if request.method == "POST":
        form = EstudianteForm(request.POST, request.FILES , instance=estudiante)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/estudiante",{"estudiante": estudiante})
            #print("vevotes")
    else:
        form = EstudianteForm()
    return render(request, "main/dashboard_student.html",{"form": form,"estudiante":estudiante, "actividades_completadas": actividad_completadas, "actividades_incompletadas": actividad_incompletadas, "group":group})

def institucionpage(response):
    estudiante = Estudiante.objects.get(name = response.user.username)
    group = str(response.user.groups.filter(name = "estudiante")[0])
    institutos = Instituciones.objects.all()
    return render(response, "main/instituciones.html", {"estudiante": estudiante, "instituciones": institutos, "group":group})
def institucionescomp(response):
    group = str(response.user.groups.filter(name = "compromiso")[0])
    compromiso = Compromiso.objects.get(name = response.user.username)
    institutos = Instituciones.objects.all()
    return render(response, "main/instituciones.html", {"compromiso": compromiso, "instituciones": institutos, "group":group})

def estudiantescomp(response):
    group = str(response.user.groups.filter(name = "compromiso")[0])
    compromiso = Compromiso.objects.get(name = response.user.username)
    estudiantes = Estudiante.objects.all()
    if response.method == "POST":
        if response.POST.get("save"):
            for estudiante in estudiantes:
                if response.POST.get("c"+ str(estudiante.id)) == "clicked":
                    estudiante.voluntariado = True
                estudiante.save()
    return render(response, "main/estudiantes.html", {"estudiantes": estudiantes, "compromiso":compromiso, "group":group})