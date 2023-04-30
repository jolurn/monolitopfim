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

from django.http import HttpResponse
import os 
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from datetime import datetime
from PIL import Image
from django.templatetags.static import static
from django.conf import settings


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
    reporteAcad = DetalleMatricula.objects.filter(matricula__alumno__usuario=request.user, estado="A").order_by('seccion__periodo__codigo')
    
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

@login_required
def generar_pdf(request):
    image_path = os.path.join(settings.STATICFILES_DIRS[0], 'pfimapp/img/logo.png')
    logo = Image.open(image_path)

    reporteAcademicos = (
        DetalleMatricula.objects
        .select_related('matricula__alumno__usuario', 'seccion__periodo', 'seccion__docente__usuario')
        .filter(matricula__alumno__usuario=request.user, estado="A")
        .order_by('seccion__periodo__codigo')
    )

    # Calcular la suma de créditos y el promedio de los promedios
    suma_creditos = 0
    promedio_general = 0
    count_promedios = 0

    for detalle in reporteAcademicos:
        suma_creditos += detalle.seccion.curso.credito
        if detalle.promedioFinal >= 12:
            promedio_general += detalle.promedioFinal
            count_promedios += 1

    promedio_general = promedio_general / count_promedios if count_promedios > 0 else 0

    #Create the HttpResponse headers with PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Platzi-student-report.pdf'
    # Create the PDF object, using the bytesIO object as its "file."
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    from datetime import datetime

    # Draw the image in the header
    logo_width, logo_height = logo.size
    aspect_ratio = logo_height / logo_width
    logo_width = 250
    logo_height = logo_width * aspect_ratio
    logo_url = request.build_absolute_uri(static('pfimapp/img/logo.png'))
    c.drawImage(logo_url, 170, 730, width=logo_width, height=logo_height)

    c.setFont('Helvetica',12)
    user_name = request.user.nombre_completos()
    c.drawString(30, 705, f'ALUMNO: {user_name}')    
    
    c.setFont('Helvetica', 12)
    c.drawString(30, 30, f'Creditos de cursos aprobados {suma_creditos}')

    # Use today() method to get current date
    current_date = datetime.today().strftime('%d/%m/%Y')
    c.drawString(480, 705, current_date)
    # start X
    c.setFont('Helvetica-Bold', 18)
    c.drawString(30, 650, 'Reporte Académico')

    # Add a subtitle with the name of the student
    c.setFont('Helvetica', 16)
    c.drawString(30, 610, f'Nombre del alumno: {user_name}')

    # Add a subtitle with the current date
    c.setFont('Helvetica', 16)
    c.drawString(30, 570, f'Fecha del reporte: {current_date}')

    # Add a table with the academic record
    data = [['Curso', 'Sección', 'Período', 'Docente', 'Promedio Final', 'Créditos']]
    for detalle in reporteAcademicos:
        data.append([
            detalle.seccion.curso.nombre,
            detalle.seccion.nombre,
            detalle.seccion.periodo.codigo,
            detalle.seccion.docente.usuario.nombre_completo(),
            f"{detalle.promedioFinal:.1f}" if detalle.promedioFinal is not None else "",
            str(detalle.seccion.curso.credito)
        ])
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    table.wrapOn(c, 500, 200)
    table.drawOn(c, 30, 480)

    # Add a section with the summary of the academic record
    c.setFont('Helvetica-Bold', 16)
    c.drawString(30, 430, 'Resumen del Reporte Académico')

    c.setFont('Helvetica', 14)
    c.drawString(30, 390, f'Créditos totales aprobados: {suma_creditos}')

    c.setFont('Helvetica', 14)
    c.drawString(30, 350, f'Promedio general de cursos aprobados: {promedio_general:.1f}')

    # Close the PDF object cleanly, and we're done.
    c.showPage()
    c.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response



