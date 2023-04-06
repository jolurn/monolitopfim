from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
# from django.contrib.auth.hashers import make_password
from django.forms import ModelForm
from pfimapp.models import CustomUser,TipoDocumento,EstadoCivil,Maestria,Sede
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm

class CustomUserForm(ModelForm):
    email = forms.CharField(label= 'Correo Electrónico (*)',max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control required'}))
    nacionalidad = forms.CharField(label='Nacionalidad (*)',max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control required'}))
    tipoDocumento = forms.ModelChoiceField(label='Tipo de Documento (*)',queryset=TipoDocumento.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control required'}))
    numeroDocumento = forms.CharField(label='Número de Documento (*)',max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control required'}))
    numeroUbigeoNacimiento = forms.CharField(label='Número de ubigeo de nacimiento (*)',max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control required'}))
    direccion = forms.CharField(label='Dirección (*)',max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control required'}))
    codigoEgresadoUNI = forms.CharField(label='Código de Egresado UNI',max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    primerNombre = forms.CharField(label='Primer Nombre (*)',max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control required'}))
    segundoNombre = forms.CharField(label='Segundo Nombre',max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellidoPaterno = forms.CharField(label='Apellido Paterno (*)',max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control required'}))
    apellidoMaterno = forms.CharField(label='Apellido Materno (*)',max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control required'}))
    estadoCivil = forms.ModelChoiceField(label='Estado Civil (*)',queryset=EstadoCivil.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control required'}))
    correoUNI = forms.CharField(label='Correo UNI',max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gradoEstudio = forms.CharField(label='Grado Estudio (*)',max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control required'}))
    universidadProcedencia = forms.CharField(label='Universidad de Procedencia (*)',max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control required'}))
    telefono = forms.CharField(label='Celular (*)',max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control required'}))
    maestria = forms.ModelChoiceField(label='Maestria que va llevar (*)',queryset=Maestria.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control required'}))
    sede = forms.ModelChoiceField(label='Sede donde va estudiar (*)',queryset=Sede.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control required'}))
    fechaNacimiento = forms.DateField(label='Fecha de Nacimiento (*)',required=False, widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}))
    
        
    class Meta:
        model = CustomUser
        fields = ['email','nacionalidad', 'tipoDocumento', 'numeroDocumento', 'numeroUbigeoNacimiento',
                  'direccion', 'codigoEgresadoUNI', 'primerNombre', 'segundoNombre',
                  'apellidoPaterno', 'apellidoMaterno', 'estadoCivil', 'correoUNI',
                  'gradoEstudio', 'universidadProcedencia', 'telefono', 'maestria',
                  'sede', 'fechaNacimiento',]
               
class CustomUserCreationForm(UserCreationForm, CustomUserForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar Contraseña'})

        self.fields['password1'].label = 'Contraseña (*)'
        self.fields['password2'].label = 'Confirmar Contraseña (*)'

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = CustomUserForm.Meta.fields



class EditarPerfilForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ['apellidoPaterno', 'apellidoMaterno', 'primerNombre', 'segundoNombre', 'email', 'correoUNI', 'gradoEstudio', 'universidadProcedencia', 'maestria', 'sede']
    

   