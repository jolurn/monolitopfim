from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import  AuthenticationForm
from pfimapp.models import ReporteEconomico,ReporteEcoConceptoPago,CustomUser,Matricula,DetalleMatricula,Alumno,Sede,Maestria,TipoDocumento,EstadoCivil
from django.contrib.auth import login, logout, authenticate
from .forms import EditarPerfilForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from pfimapp.forms import CustomUserCreationForm
  

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

@login_required
def edit_user(request):
    user = get_object_or_404(CustomUser, id=request.user.id)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('home')
    else:
        form = PasswordChangeForm(user)
    return render(request, 'editUser.html', {'form': form})

@login_required
def reporteEconomico(request):
    alumno_login = Alumno.objects.get(usuario=request.user, estado="A")

    reporteEcon = ReporteEconomico.objects.filter(alumno__usuario=request.user, estado="A")
    detalleRepoEco = ReporteEcoConceptoPago.objects.filter(reporteEconomico=reporteEcon.first(), estado="A")

    return render(request, 'reporteEconomico.html',{'reporteEconomicos':detalleRepoEco,'alumno_login':alumno_login})

@login_required
def reporteAcademico(request):
    alumno_login = Alumno.objects.get(usuario=request.user, estado="A")

    reporteEcon = ReporteEconomico.objects.filter(alumno__usuario=request.user, estado="A")
    if reporteEcon.exists():
        detalleRepoEco = ReporteEcoConceptoPago.objects.filter(reporteEconomico=reporteEcon.first(), estado="A")
    else:
        detalleRepoEco = []

    detalleAcademico = DetalleMatricula.objects.filter(matricula__alumno__usuario=request.user, estado="A")
    
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
   
    return render(request, 'reporteAcademico.html', {'reporteAcademicos': detalleAcademico, 'alumno_login':alumno_login,'reporteEconomicos': detalleRepoEco, 'hay_registro_nulo': hay_registro_nulo, 'hay_estadoBoletaPag_pendiente':hay_estadoBoletaPag_pendiente})

@login_required
def perfil(request):
    maestrias = Maestria.objects.all()
    sedes = Sede.objects.all()
    tipoDocumentos = TipoDocumento.objects.all()
    estadoCivils = EstadoCivil.objects.all()
    context = {
        'maestrias': maestrias,
        'sedes': sedes,
        'tipoDocumentos' : tipoDocumentos,
        'estadoCivils': estadoCivils,
        'form': EditarPerfilForm(instance=request.user)
    }
    return render(request, 'perfil.html', context)


@login_required
def editar_perfil(request):
    
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado con éxito!')
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=request.user)
    return render(request, 'perfil.html', {'form': form})    

@login_required
def reporteMatricula(request):  
    matriculas = Matricula.objects.filter(alumno__usuario=request.user, estado="A")           

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

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
        'form': AuthenticationForm
    })
    else:
        user = authenticate(request, email=request.POST['email'],password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{'form': AuthenticationForm, 'error': 'Username or password is incorrect'})
        else:
            login(request, user)
            return redirect('reporteEconomico')

