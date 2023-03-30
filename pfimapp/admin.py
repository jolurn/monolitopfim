from django.contrib import admin
from pfimapp.models import CustomUser,TipoDocumento,Maestria,EstadoCivil,Sede

# Register your models here.
# class UserAdmin(admin.ModelAdmin):
#     search_fields = ['dni', 'last_name']
#     ordering = ['last_name']
#     list_display = ('username', 'first_name', 'last_name',
#                     'email', 'dni', 'password')

#     def save_model(self, request, obj, form, change):
#         if obj.password.startswith('pbkdf2'):
#             obj.password = obj.password
#         else:
#             obj.set_password(obj.password)
#         super().save_model(request, obj, form, change)


admin.site.register(CustomUser)

class TipoDocumentoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    ordering = ['nombre']
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado',
               'fechaElimnado', 'usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro','usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('nombre', 'estado', 'fechaRegistro')

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)

admin.site.register(TipoDocumento, TipoDocumentoAdmin)

class SedeAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    ordering = ['nombre']
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado',
               'fechaElimnado', 'usuarioPosgradoFIM', 'ipUsuario')
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
    ordering = ['nombre']
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado',
               'fechaElimnado', 'usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('nombre', 'estado', 'fechaRegistro')

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)

admin.site.register(EstadoCivil, EstadoCivilAdmin)


class MaestriaAdmin(admin.ModelAdmin):
    search_fields = ['codigo']
    ordering = ['codigo']
    # --- poner en solo lectura los input ---
    exclude = ('fechaRegistro', 'fechaModificado',
               'fechaElimnado', 'usuarioPosgradoFIM', 'ipUsuario')
    readonly_fields = ('fechaRegistro', 'usuarioPosgradoFIM', 'ipUsuario')
# ----- Fin poner en solo lectura los input -----
    list_display = ('codigo', 'nombre', 'estado', 'fechaRegistro')

    def save_model(self, request, obj, form, change):
        # request.user es el usuario autenticado en ese momento

        obj.usuarioPosgradoFIM = request.user.apellidoPaterno+' '+request.user.apellidoMaterno+' '+request.user.primerNombre
        super().save_model(request, obj, form, change)


admin.site.register(Maestria, MaestriaAdmin)


