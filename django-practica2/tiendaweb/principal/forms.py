
from django import forms
from .models import Producto, Cliente

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'imagen', 'precio', 'stock', 'descripcion']


class DeleteProductoForm(forms.Form):
    confirm = forms.BooleanField(label="Confirmar eliminación")

class ActualizarNombreUsuarioForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['username']