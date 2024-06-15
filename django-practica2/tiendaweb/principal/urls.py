from django.urls import path
from . import views

urlpatterns = [
path('',views.home, name='inicio'),
path('registro/',views.registro, name='registro'),
path('login/',views.inicio_sesion, name='login'),
path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
path('autenticadovista/',views.autenticadovista, name='autenticadovista')
]
