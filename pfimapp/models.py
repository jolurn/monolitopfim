from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
# Create your models here.

Es1 = 'A'
Es2 = 'I'
ESTADO_OFERTA = [
    (Es1, 'Activo'),
    (Es2, 'Inactivo')
]

class EstadoCivil(models.Model):

    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=datetime.now())    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name_plural = "Estado Civil"

class Sede(models.Model):

    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=datetime.now())    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[
                                 0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(
        null=True, blank=True, max_length=200)

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name_plural = "Sede"

class Maestria(models.Model):

    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=datetime.now())    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[
                                 0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(
        null=True, blank=True, max_length=200)

    def __str__(self):
        return "{} - {}".format(self.codigo, self.nombre)

    class Meta:
        verbose_name_plural = "Maestrias"

class TipoDocumento(models.Model):

    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=datetime.now())
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)
    fechaElimnado = models.DateField(null=True, blank=True)
    ipUsuario = models.CharField(null=True, default=s.getsockname()[
                                 0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(
        null=True, blank=True, max_length=200)

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name_plural = "Tipo de Documentos"

class UsuarioManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El Email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Los superusuarios deben tener is_staff=True')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Los superusuarios deben tener is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    nacionalidad = models.CharField(max_length=100)
    tipoDocumento = models.ForeignKey(TipoDocumento, null=True, on_delete=models.SET_NULL)
    numeroDocumento = models.CharField(max_length=100,unique=True)
    numeroUbigeoNacimiento = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    codigoEgresadoUNI = models.CharField(max_length=20,null=True, blank=True)    
    primerNombre = models.CharField(max_length=100)
    segundoNombre = models.CharField(max_length=100, null=True, blank=True)
    apellidoPaterno = models.CharField(max_length=100)
    apellidoMaterno = models.CharField(max_length=100)    
    estadoCivil = models.ForeignKey(EstadoCivil, null=True, on_delete=models.SET_NULL)
    correoUNI = models.CharField(null=True, blank=True,max_length=100)
    gradoEstudio = models.CharField(max_length=200)
    universidadProcedencia = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    maestria = models.ForeignKey(Maestria, null=True, on_delete=models.SET_NULL)
    sede = models.ForeignKey(Sede, null=True, on_delete=models.SET_NULL)
    fechaNacimiento = models.DateField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['primerNombre', 'segundoNombre','apellidoPaterno','apellidoMaterno']

    def __str__(self):
        return self.email
