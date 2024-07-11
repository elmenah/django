from django.urls import path
from . import views

urlpatterns = [
path('',views.home, name='inicio'),
path('registro/',views.registro, name='registro'),
path('tyc/',views.tyc, name='terminos'),
path('ofertass/',views.ofertas, name='ofertas'),
path('login/',views.inicio_sesion, name='login'),
path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
path('contacto/',views.contact, name='contacto'),
path('perfil/',views.perfilvista, name='perfil'),
path('productos/', views.lista_productos, name='lista_productos'),
path('add_producto/', views.add_producto, name='add_producto'),
path('carrito/', views.carrito, name='carro'),
path('delete_producto/<int:producto_id>/', views.delete_producto, name='delete_producto'),
 path('actualizar_stock/', views.actualizar_stock, name='actualizar_stock')


]
