from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from main.models import Estudiante, Instituciones, Compromiso
# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        print(response.POST.get("type_of"))
        new_group = Group.objects.get_or_create(name = response.POST.get("type_of") )
        print(response.method)
        if form.is_valid():
            form.save()
            new_group = Group.objects.get(name__exact = response.POST.get("type_of"))
            user = User.objects.get(username = response.POST.get("username"))
            print(str(new_group) == "instituto")
            user.groups.add(new_group)
            if str(new_group)  ==  "estudiante":
                e = Estudiante(name = response.POST.get("username"), horas = 0, celular = "", voluntariado = False)
                print(e)
                e.save()
            elif str(new_group) == "instituto":
                i = Instituciones(name = response.POST.get("username"))
                i.save()
                print(i)
            elif str(new_group) == "compromiso":
                c = Compromiso(name = response.POST.get("username"))
                c.save()
                print(c)
        return redirect("/login")
    else:
        form = RegisterForm()
    compromiso = Compromiso.objects.get(name = response.user.username)
    group = str(response.user.groups.filter(name = "compromiso")[0])
    return render(response,"register/register.html",{"form":form, "compromiso" : compromiso, "group": group}) #{"compromiso":compromiso}#)