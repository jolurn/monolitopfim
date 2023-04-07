from django.contrib import admin
from pfimapp.models import DetalleMatricula,Matricula,Seccion,Docente,Curso,CustomUser,TipoDocumento,Maestria,EstadoCivil,Sede,ReporteEcoConceptoPago,ReporteEconomico,ConceptoPago,Periodo,Alumno,EstadoAcademico,EstadoBoletaP

# Register your models here.
class SeccionAdmin(admin.ModelAdmin):
    # Para que sea mas facil de encontrar a la hora de crear una matricula
    search_fields = ['periodo__codigo', 'maestria__codigo', 'curso__codigo']
    autocomplete_fields = ['curso', 'periodo', 'docente', 'maestria']
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('curso', 'docente', 'periodo', 'maestria',
                    'aulaWeb', 'estado', 'fechaRegistro')

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)


admin.site.register(Seccion, SeccionAdmin)

class DocenteAdmin(admin.ModelAdmin):
    search_fields = ['usuario__apellidoPaterno']
    autocomplete_fields = ['usuario','maestria']
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('usuario', 'maestria', 'estado', 'fechaRegistro')

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)


admin.site.register(Docente, DocenteAdmin)

class CursoAdmin(admin.ModelAdmin):
    search_fields = ['codigo']
    ordering = ['codigo']
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('codigo', 'nombre', 'credito', 'estado', 'fechaRegistro')

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)


admin.site.register(Curso, CursoAdmin)

class UserAdmin(admin.ModelAdmin):
    search_fields = ['apellidoPaterno', 'email', 'numeroDocumento']
    ordering = ['apellidoPaterno']
    list_display = ('tipoDocumento', 'numeroDocumento', 'primerNombre', 'segundoNombre',
                    'apellidoPaterno', 'apellidoMaterno', 'email')

admin.site.register(CustomUser, UserAdmin)

class PeriodoAdmin(admin.ModelAdmin):
    search_fields = ['codigo']
    ordering = ['codigo']
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('codigo', 'nombre', 'estado', 'fechaRegistro')

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)


admin.site.register(Periodo, PeriodoAdmin)

class TipoDocumentoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    ordering = ['nombre']
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro','usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('nombre', 'estado', 'fechaRegistro')

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)

admin.site.register(TipoDocumento, TipoDocumentoAdmin)

class EstadoBoletaPAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    ordering = ['nombre']
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('nombre', 'estado', 'fechaRegistro')

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)


admin.site.register(EstadoBoletaP, EstadoBoletaPAdmin)

class SedeAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    ordering = ['nombre']
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('nombre', 'estado', 'fechaRegistro')

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)

admin.site.register(Sede, SedeAdmin)

class EstadoCivilAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    ordering = ['nombre','fechaRegistro']
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('nombre', 'estado', 'fechaRegistro')

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)

admin.site.register(EstadoCivil, EstadoCivilAdmin)

class EstadoAcademicoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    ordering = ['nombre']
    
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('nombre', 'estado', 'fechaRegistro', 'usuarioPosgradoFIM')

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)

admin.site.register(EstadoAcademico, EstadoAcademicoAdmin)


class MaestriaAdmin(admin.ModelAdmin):
    search_fields = ['codigo']
    ordering = ['codigo']
   
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('codigo', 'nombre', 'estado', 'fechaRegistro')

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)


admin.site.register(Maestria, MaestriaAdmin)

class AlumnoAdmin(admin.ModelAdmin):
    search_fields = ['usuario__apellidoPaterno', 'usuario__numeroDocumento']
    autocomplete_fields = ['usuario', 'periodoDeIngreso','maestria']
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('usuario', 'maestria', 'periodoDeIngreso',
                    'codigoUniPreGrado', 'estadoAcademico', 'estado', 'fechaRegistro')

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)


admin.site.register(Alumno, AlumnoAdmin)

class ConceptoPagoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    ordering = ['nombre']
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('nombre', 'estado', 'fechaRegistro')

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)


admin.site.register(ConceptoPago, ConceptoPagoAdmin)

class ReporteEcoConceptoPagoAdmin(admin.TabularInline):
    model = ReporteEcoConceptoPago
    extra = 0
  
    autocomplete_fields = ['conceptoPago', 'periodo']
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)


class ReporteEconomicoAdmin(admin.ModelAdmin):
    search_fields = ['alumno__usuario__apellidoPaterno',
                     'alumno__usuario__numeroDocumento']
    autocomplete_fields = ['alumno']
    inlines = [ReporteEcoConceptoPagoAdmin, ]
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('alumno', 'estado', 'fechaRegistro')
    filter_horizontal = ['conceptoPago']

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)


admin.site.register(ReporteEconomico, ReporteEconomicoAdmin)

class DetalleMatriculaAdmin(admin.TabularInline):
    model = DetalleMatricula
    extra = 1
    autocomplete_fields = ['seccion']
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado', 'usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)


class MatriculaAdmin(admin.ModelAdmin):
    search_fields = ['alumno__usuario__apellidoPaterno',
                     'alumno__usuario__numeroDocumento', 'periodo__codigo']
    autocomplete_fields = ['alumno', 'periodo']
    inlines = [DetalleMatriculaAdmin, ]
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'fechaModificado','usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('alumno', 'periodo', 'estado', 'fechaRegistro')
    filter_horizontal = ['seccion']

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)


admin.site.register(Matricula, MatriculaAdmin)