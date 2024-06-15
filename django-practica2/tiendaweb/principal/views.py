from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, 'index.html')

def registro(request):
    try:
        if request.method == "POST":
            usuario = request.POST.get("usuario")
            correo = request.POST.get("correo")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if password1 == password2:
                messages.success(request,'Usuario registrado correctamente')
                user= User.objects.create_user(username=usuario,email=correo,password=password1)
                user.save()
                print('Usuario guardado')
                return redirect('login')
            else:
                return render(request,'registro.html',{'mensaje':'Contraseñas no coinciden'})
        elif request.method == 'GET':
            return render(request,'registro.html')
        
    except IntegrityError as valorUnico:
        print(valorUnico)
        return render(request,'registro.html',{'mensaje':'Usuario ya existe !'})
    except Exception as mensaje:
        print(mensaje)

def inicio_sesion(request):
    try:
        if request.method == "POST":
            usuario = request.POST.get("usuariologin")
            contraseña = request.POST.get("password1login")
            user = authenticate(request, username=usuario, password=contraseña)
            if user is not None:
                messages.success(request,'Sesion iniciada correctamente')
                login(request, user)
                print('Sesion iniciada')
                return redirect('inicio')
            
            else:
                return render(request, 'login.html', {'mensaje': 'Usuario o contraseña incorrectos'})
        elif request.method == 'GET':
            return render(request, 'login.html')
    except Exception as e:
        print(e)
        return render(request, 'login.html', {'mensaje': 'Se produjo un error al procesar su solicitud'})


def cerrar_sesion(request):
    logout(request)
    # Redirige a la página de inicio u otra página después de cerrar sesión
    return redirect('inicio')

def autenticadovista(request):
 return render(request, 'home.html')


    