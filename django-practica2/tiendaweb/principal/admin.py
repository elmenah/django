from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Cliente,Producto
# Register your models here.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'fecha_nacimiento', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'fecha_nacimiento')

admin.site.register(Producto)

