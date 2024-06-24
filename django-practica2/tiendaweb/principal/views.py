from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.http import HttpResponse
from django.contrib import messages
from .models import Cliente,Producto
from datetime import datetime,date,timedelta

from .forms import ProductoForm,DeleteProductoForm


# Create your views here.

def home(request):
    return render(request, 'home.html')



def registro(request):
    try:
        if request.method == "POST": #Crear modelo de usuario cliente para almacenar fecha de nacimiento solo si es necesario
            usuario = request.POST.get("usuario")  
            correo = request.POST.get("correo")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            fecha = request.POST.get("fecha")
            fechanacimiento = datetime.strptime(fecha, '%Y-%m-%d').date()

            fechahoy = date.today()

             # Calcular la fecha mínima para ser mayor de edad (18 años)
            fecha_mayor_edad = fechahoy - timedelta(days=365*18)
             # Validar que la fecha de nacimiento sea menor que la fecha mínima
            if fechanacimiento > fecha_mayor_edad:
                messages.error(request, 'Debes ser mayor de 18 años para registrarte.')
                return render(request, 'registro.html')

            
            
            if password1 == password2 :
                if fechanacimiento < fecha_mayor_edad:
                    messages.success(request,'Usuario registrado correctamente')
                    cliente= Cliente.objects.create_user(username=usuario,email=correo,password=password1,fecha_nacimiento=fecha)  
                    cliente.save()
                    print('Usuario guardado')
               
                    return redirect('login')
            else:
                return render(request,'registro.html',{'mensaje':'Contraseñas no coinciden o fecha de nacimiento no es mayor de edad'})
        elif request.method == 'GET':
            return render(request,'registro.html')
        
    except IntegrityError as valorUnico:
        print(valorUnico)
        return render(request,'registro.html',{'mensaje':'Usuario ya existe !'})
    except Exception as mensaje:
        print(mensaje)

def inicio_sesion(request):
    if request.method == "POST":
        usuario = request.POST.get("usuariologin")
        contraseña = request.POST.get("password1login")

        if not usuario or not contraseña:
            messages.error(request, 'Debe proporcionar un nombre de usuario y una contraseña')
            return redirect('login')

        try:
            cliente = authenticate(request, username=usuario, password=contraseña)
            if cliente is not None:
                login(request, cliente)
                messages.success(request, 'Sesión iniciada correctamente')
                return redirect('inicio')
            else:
                messages.error(request, 'Usuario o contraseña inválidos')
                return redirect('login')
        except Exception as e:
            messages.error(request, f'Se produjo un error al procesar su solicitud: {str(e)}')
            return redirect('login')
    
    elif request.method == 'GET':
        return render(request, 'login.html')
    
    else:
        messages.error(request, 'Método no permitido')
        return redirect('login')

def cerrar_sesion(request):
    logout(request)
    # Redirige a la página de inicio u otra página después de cerrar sesión
    return redirect('inicio')

def contact(request):
    return render(request, 'contacto.html')

def perfilvista(request):
    # Obtener el usuario autenticado actual
    user = request.user  # Esto asume que estás usando el sistema de autenticación de Django
    context = {
        'user': user
    }
    return render(request, 'perfil.html', context)

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'producto.html', {'productos': productos})


def add_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')  # Redirige a una vista que liste los productos, cambia esto según tu configuración
    else:
        form = ProductoForm()
    
    return render(request, 'add_producto.html', {'form': form})

def delete_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == "POST":
        delete_form = DeleteProductoForm(request.POST)
        if delete_form.is_valid() and delete_form.cleaned_data['confirm']:
            producto.delete()
            return redirect('lista_productos')  # Redirige a la lista de productos después de eliminar uno
    else:
        delete_form = DeleteProductoForm()
    
    return render(request, 'delete_producto.html', {
        'delete_form': delete_form,
        'producto': producto
    })