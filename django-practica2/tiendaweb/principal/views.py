from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.http import HttpResponse
from django.contrib import messages
from .models import Cliente,Producto
from datetime import datetime,date,timedelta
from django.contrib.auth.decorators import login_required

from .forms import ProductoForm,DeleteProductoForm, ActualizarNombreUsuarioForm




def home(request): #Vista Home
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

            
              # Verificar si el usuario ya existe
            if Cliente.objects.filter(username=usuario).exists():
                messages.error(request, 'El nombre de usuario ya existe. Elija otro.')
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
            # Verificar si el usuario existe
            try:
                cliente = Cliente.objects.get(username=usuario)
            except Cliente.DoesNotExist:
                messages.error(request, 'El usuario no existe')
                return redirect('login')

            # Intentar autenticar al usuario
            cliente_autenticado = authenticate(request, username=usuario, password=contraseña)
            if cliente_autenticado is not None:
                login(request, cliente_autenticado)
                
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

def contact(request): #Vista Contacto
    return render(request, 'contacto.html')


  

def lista_productos(request):#Vista que llega a la pagina producto donde obtiene todos los productos en la variable productos
    productos = Producto.objects.all()
    return render(request, 'producto.html', {'productos': productos})


def add_producto(request):   # Vista para agregar un producto 
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)#La vista add producto va a mostrar el formulario ProductoForm
        if form.is_valid():
            form.save()
            return redirect('lista_productos')  # Redirige a una vista que liste los productos
    else:
        form = ProductoForm()
    
    return render(request, 'add_producto.html', {'form': form})

def delete_producto(request, producto_id): # Vista para borrar un producto por ID
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



def carrito(request): # Renderiza el template carritox
    return render(request, 'carritox.html')

@login_required # Requiere estar logeado
def perfilvista(request):
    user = request.user
    if request.method == 'POST':
        if 'update' in request.POST: # Si el metodo o name es update al hacer post
            form = ActualizarNombreUsuarioForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Correo modificado correctamente')
                return redirect('perfil')  # Redirige a la página de inicio 
        elif 'delete' in request.POST: # Si el metodo o name es delete al hacer post
            user.delete()
            messages.success(request, 'Cuenta eliminada correctamente')
            return redirect('inicio')  # Redirige a la página de inicio
    else:
        form = ActualizarNombreUsuarioForm(instance=user)
    
    return render(request, 'perfil.html', {'form': form})

def tyc(request):
    return render(request, 'T&C.html')

def ofertas(request):
    return render(request, 'ofertas.html')