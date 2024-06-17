from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
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

class Cliente(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, default='')  # Aquí se define un valor predeterminado vacío ('') para el campo email
    fecha_nacimiento = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'fecha_nacimiento']

    objects = ClienteManager()

    def __str__(self):
        return self.username

    @property
    def is_superuser(self):
        return self.is_staff

    @property
    def is_staff(self):
        return self.is_staff