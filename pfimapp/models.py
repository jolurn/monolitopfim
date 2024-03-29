from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

Es1 = 'A'
Es2 = 'I'
ESTADO_OFERTA = [
    (Es1, 'Activo'),
    (Es2, 'Inactivo')
]

class EstadoCivil(models.Model):

    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name_plural = "Estado Civil"

class Sede(models.Model):

    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)  
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name_plural = "Sede"

class Maestria(models.Model):

    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)   
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return "{} - {}".format(self.codigo, self.nombre)

    class Meta:
        verbose_name_plural = "Maestrias"

class TipoDocumento(models.Model):

    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name_plural = "Tipo de Documentos"

class UsuarioManager(BaseUserManager):

    def create_user(self, email, primerNombre, apellidoPaterno, segundoNombre, apellidoMaterno, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        if not primerNombre:
            raise ValueError('El usuario debe tener un primer nombre')
        if not segundoNombre:
            raise ValueError('El usuario debe tener un segundo nombre')        
        if not apellidoPaterno:
            raise ValueError('El usuario debe tener un apellido paterno')
        if not apellidoMaterno:
            raise ValueError('El usuario debe tener un apellido materno')

        user = self.model(
            email=self.normalize_email(email),
            primerNombre=primerNombre,
            segundoNombre=segundoNombre,
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, primerNombre, segundoNombre,apellidoPaterno,apellidoMaterno, password):
        user = self.create_user(
            email=self.normalize_email(email),
            primerNombre=primerNombre,
            segundoNombre=segundoNombre,
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=100,unique=True, error_messages={'unique': 'Este correo electrónico ya está en uso.'})
    nacionalidad = models.CharField(max_length=100)
    tipoDocumento = models.ForeignKey(TipoDocumento, null=True, on_delete=models.SET_NULL)
    numeroDocumento = models.CharField(max_length=100,unique=True, error_messages={'unique': 'Este DNI ya está en uso.'})
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
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
  
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['primerNombre', 'segundoNombre','apellidoPaterno','apellidoMaterno']

   
        
    def nombre_completos(self):
        if self.segundoNombre:
            return "{} {} {} {}".format(self.apellidoPaterno, self.apellidoMaterno, self.primerNombre, self.segundoNombre)
        else:
            return "{} {} {}".format(self.apellidoPaterno, self.apellidoMaterno, self.primerNombre)


    def __str__(self):
        return self.nombre_completos()
  
    class Meta:
        verbose_name_plural = "Usuarios"

class EstadoBoletaP(models.Model):

    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Estados Boletas Pagos"


class ConceptoPago(models.Model):

    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Conceptos de Pagos"

class EstadoAcademico(models.Model):

    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name_plural = "Estados Academico"

class Periodo(models.Model):

    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.codigo

    class Meta:
        verbose_name_plural = "Periodos"

class Alumno(models.Model):

    usuario = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    maestria = models.ForeignKey(Maestria, null=True, on_delete=models.SET_NULL)
    periodoDeIngreso = models.ForeignKey(Periodo, null=True, blank=True, on_delete=models.SET_NULL)
    codigoUniPreGrado = models.CharField(max_length=10, null=True, blank=True)
    codigoAlumPFIM = models.CharField(max_length=15, null=True, blank=True)
    estadoAcademico = models.ForeignKey(EstadoAcademico, null=True, on_delete=models.SET_NULL)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)
    
    def nombre_completo(self):
        if self.usuario.segundoNombre:
            return "{} {} {} {}".format(self.usuario.apellidoPaterno, self.usuario.apellidoMaterno, self.usuario.primerNombre, self.usuario.segundoNombre)
        else:
            return "{} {} {}".format(self.usuario.apellidoPaterno, self.usuario.apellidoMaterno, self.usuario.primerNombre)
        
    def __str__(self):
        return self.nombre_completo()

    class Meta:
        verbose_name_plural = "Alumnos"

class ReporteEconomico(models.Model):

    alumno = models.ForeignKey(Alumno, null=True, on_delete=models.SET_NULL)
    conceptoPago = models.ManyToManyField(ConceptoPago, through='ReporteEcoConceptoPago', blank=True,)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    class Meta:

        verbose_name_plural = "Reportes Economicos"


class ReporteEcoConceptoPago(models.Model):

    reporteEconomico = models.ForeignKey(ReporteEconomico, null=True, on_delete=models.SET_NULL)
    conceptoPago = models.ForeignKey(ConceptoPago, null=True, on_delete=models.SET_NULL)
    periodo = models.ForeignKey(Periodo, null=True, on_delete=models.SET_NULL)
    monto = models.FloatField()
    numeroRecibo = models.CharField(max_length=100, null=True, blank=True)
    estadoBoletaPago = models.ForeignKey(EstadoBoletaP, null=True, on_delete=models.SET_NULL)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

class Curso(models.Model):

    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    credito = models.IntegerField()
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return "{} - {}".format(self.codigo, self.nombre)

    class Meta:
        verbose_name_plural = "Cursos"

class Docente(models.Model):

    usuario = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    maestria = models.ForeignKey(Maestria, null=True, on_delete=models.SET_NULL)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def nombre_completo(self):
        return "{} {} {} {}, {}".format(self.usuario.apellidoPaterno, self.usuario.apellidoMaterno, self.usuario.primerNombre, self.usuario.segundoNombre, self.maestria.codigo)

    def __str__(self):
        return self.nombre_completo()

    class Meta:
        verbose_name_plural = "Docentes"

class Seccion(models.Model):

    maestria = models.ForeignKey(Maestria, null=True, on_delete=models.SET_NULL)
    periodo = models.ForeignKey(Periodo, null=True, on_delete=models.SET_NULL)
    curso = models.ForeignKey(Curso, null=True, on_delete=models.SET_NULL)
    docente = models.ForeignKey(Docente, null=True, on_delete=models.SET_NULL)
    aulaWeb = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def nombre_completo(self):
        return "{} - {} {} - {} {} {}".format(self.periodo.codigo, self.maestria.codigo, self.curso.codigo, self.curso.nombre, self.docente.usuario.apellidoPaterno, self.docente.usuario.apellidoMaterno, self.docente.usuario.primerNombre)

    def __str__(self):
        return self.nombre_completo()

    class Meta:
        verbose_name_plural = "Secciones"

class Matricula(models.Model):

    alumno = models.ForeignKey(Alumno, null=True, on_delete=models.SET_NULL)
    seccion = models.ManyToManyField(Seccion, through='DetalleMatricula', blank=True,)
    periodo = models.ForeignKey(Periodo, null=True, on_delete=models.SET_NULL)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def nombre_completo(self):
        return "{} {}, {} {}".format(self.alumno.usuario.apellidoPaterno, self.alumno.usuario.apellidoMaterno, self.alumno.usuario.primerNombre, self.alumno.usuario.segundoNombre)

    def __str__(self):
        return self.nombre_completo()

    class Meta:
        verbose_name_plural = "Matriculas"


class DetalleMatricula(models.Model):

    matricula = models.ForeignKey(Matricula, null=True, on_delete=models.SET_NULL)
    seccion = models.ForeignKey(Seccion, null=True, on_delete=models.SET_NULL)
    promedioTrabajos = models.FloatField(null=True, blank=True)
    examenParcial = models.FloatField(null=True, blank=True)
    examenFinal = models.FloatField(null=True, blank=True)
    promedioFinal = models.FloatField(null=True, blank=True)
    retirado = models.BooleanField(default=False)
    estado = models.CharField(max_length=1, choices=ESTADO_OFERTA, default='A')
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    
    def __str__(self):
        return "{}  {}, {} {}".format(self.matricula.alumno.usuario.apellidoPaterno, self.matricula.alumno.usuario.apellidoMaterno, self.seccion.curso, self.seccion.periodo)

    class Meta:
        verbose_name_plural = "Detalle de Matriculas"