from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class ClienteManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, fecha_nacimiento=None, **extra_fields):
        if not username:
            raise ValueError('El nombre de usuario debe ser establecido')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, fecha_nacimiento=fecha_nacimiento, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, fecha_nacimiento=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, fecha_nacimiento, **extra_fields)

class Cliente(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, default='')  
    fecha_nacimiento = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'fecha_nacimiento']

    objects = ClienteManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        # Si el usuario es superusuario, tiene todos los permisos
        if self.is_superuser:
            return True
        
        return self.is_staff

    def has_module_perms(self, app_label):
        # Si el usuario es superusuario, tiene permisos para todas las aplicaciones
        if self.is_superuser:
            return True
        
        return self.is_staff
    


class Producto(models.Model):
    
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    descripcion = models.TextField(default='')

    def __str__(self):
        return self.nombre