from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import  AuthenticationForm
from pfimapp.models import ReporteEconomico,ReporteEcoConceptoPago,CustomUser,Matricula,DetalleMatricula,Alumno,Sede,Maestria,TipoDocumento,EstadoCivil
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from pfimapp.forms import CustomUserCreationForm,CustomUserForm
from django.views.generic import UpdateView
from .forms import CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView

def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('reporteEconomico')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class CustomUserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'customuser_form.html'
    form_class = CustomUserForm
    success_url = reverse_lazy('home')

@login_required
def reporteEconomico(request):
    try:
        alumno_login = Alumno.objects.get(usuario=request.user, estado="A")                
    except Alumno.DoesNotExist:
        alumno_login = None
    
    reporteEcon = ReporteEconomico.objects.filter(alumno__usuario=request.user, estado="A")
    if reporteEcon:
        detalleRepoEco = ReporteEcoConceptoPago.objects.filter(reporteEconomico=reporteEcon.first(), estado="A")
    else:
        detalleRepoEco = []

    return render(request, 'reporteEconomico.html', {'reporteEconomicos': detalleRepoEco, 'alumno_login': alumno_login})


@login_required
def reporteAcademico(request):
    reporteAcad = DetalleMatricula.objects.filter(matricula__alumno__usuario=request.user, estado="A")
    
    if reporteAcad.exists():
        alumno_login = Alumno.objects.get(usuario=request.user, estado="A")

        reporteEcon = ReporteEconomico.objects.filter(alumno__usuario=request.user, estado="A")
        if reporteEcon.exists():
            detalleRepoEco = ReporteEcoConceptoPago.objects.filter(reporteEconomico=reporteEcon.first(), estado="A")
        else:
            detalleRepoEco = []

        # Comprobar si hay algún registro con el campo 'numeroRecibo' nulo
        hay_registro_nulo = False
        hay_estadoBoletaPag_pendiente = False
        for detalle in detalleRepoEco:
            if detalle.numeroRecibo is None:
                hay_registro_nulo = True
                break
            elif detalle.estadoBoletaPago_id == 2:
                hay_estadoBoletaPag_pendiente = True
                break

        return render(request, 'reporteAcademico.html', {'reporteAcademicos': reporteAcad, 'alumno_login':alumno_login,'reporteEconomicos': detalleRepoEco, 'hay_registro_nulo': hay_registro_nulo, 'hay_estadoBoletaPag_pendiente':hay_estadoBoletaPag_pendiente})
    else:
        return render(request, 'reporteAcademico.html', {'reporteAcademicos': reporteAcad})

@login_required
def reporteMatricula(request):
    try:
        matriculas = Matricula.objects.filter(alumno__usuario=request.user, estado="A")
    except Matricula.DoesNotExist:
        matriculas = []

    return render(request, 'matricula.html', {'matriculas': matriculas})


@login_required
def detalleMatricula(request, matricula_id):
    detalleAcademico = DetalleMatricula.objects.filter(matricula=matricula_id)
    alumno_login = Alumno.objects.get(usuario=request.user, estado="A")
    
    if detalleAcademico.exists():
        periodo = detalleAcademico.first().seccion.periodo
    else:
        periodo = None

    return render(request, 'detalleMatricula.html', {'detalleAcademico': detalleAcademico, 'periodo': periodo, 'alumno_login':alumno_login})

@login_required
def signout(request):
    logout(request)
    return redirect('home')


class CustomLoginView(LoginView):
    template_name = 'signin.html'
    form_class = CustomAuthenticationForm
    success_url = '/'

class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')
    template_name = 'change_password.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        return response



