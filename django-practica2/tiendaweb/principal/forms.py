
from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'imagen', 'precio', 'stock', 'descripcion']

# principal/forms.py (continuación)
class DeleteProductoForm(forms.Form):
    confirm = forms.BooleanField(label="Confirmar eliminación")