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

    reporteAcademicos = DetalleMatricula.objects.filter(matricula__alumno__usuario=request.user, estado="A").order_by('seccion__periodo__codigo')
    
    # Calcula el promedio de los promedios mayores o iguales a 12
    promedios_altos = DetalleMatricula.objects.filter(matricula__alumno__usuario=request.user, estado="A", promedioFinal__gte=12)
    promedios = [detalle.promedioFinal for detalle in promedios_altos]
    promedio_general = sum(promedios) / len(promedios) if len(promedios) > 0 else 0
    # Calcular la suma de créditos
    suma_creditos = sum(detalle.seccion.curso.credito for detalle in promedios_altos)
    
    #Create the HttpResponse headers with PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Platzi-student-report.pdf'
    # Create the PDF object, using the bytesIO object as its "file."
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    from datetime import datetime

    # ...

    # Header
    # c.setLineWidth(.3)
    # c.setFont('Helvetica', 22)
    # c.drawString(30, 750, 'Posgrado FIM UNI')

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
    
    # Mostrar el promedio general
    # c.setFont('Helvetica',12)
    # c.drawString(30, 50, f'Promedio de cursos aprobados: {promedio_general:.2f}') 

    c.setFont('Helvetica', 12)
    c.drawString(30, 30, f'Creditos de cursos aprobados {suma_creditos}')

    # Use today() method to get current date
    current_date = datetime.today().strftime('%d/%m/%Y')
    c.drawString(480, 705, current_date)
    # start X, height end y, height
    c.line(460,702,560,702)
  
    #table header
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSize = 10
        
    # Table data
    # encabezado de la tabla
    header = [    'Periodo','Código','Curso','Crédito','Docente', 'Promedio','Retirado']

    # datos de la tabla
    data = [    header,]
    high = 650
    for detalle in reporteAcademicos:
        student = [
            str(detalle.seccion.periodo.codigo),
            str(detalle.seccion.curso.codigo),
            str(detalle.seccion.curso.nombre),
            str(detalle.seccion.curso.credito),
            str(detalle.seccion.docente.usuario.nombre_completos()),            
            str(detalle.promedioFinal),
            str(detalle.retirado),
        ]
        data.append(student)
        high = high - 18
    #table size
    width, height = A4
    table = Table(data, colWidths=[1.4 * cm,0.9 * cm, 8.5 * cm,0.9 * cm, 4.5 * cm, 1.4 *cm, 1.4*cm])
    table.setStyle(TableStyle([
    # Estilo de las celdas de la tabla
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Estilo de fuente
        ('FONTSIZE', (0, 0), (-1, -1), 7.2),  # Tamaño de fuente
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Color de fondo de la fila del encabezado
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Color de texto de la fila del encabezado
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Alineación del texto en la fila del encabezado
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Estilo de fuente
        ('FONTSIZE', (0, 1), (-1, -1), 4.5),  # Tamaño de fuente
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación del texto en todas las celdas
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alineación vertical del texto en todas las celdas
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Estilo de las líneas de la tabla
    ]))
    # pdf size
    table.wrapOn(c, width, height)
    table.drawOn(c, 30, high)
    c.showPage() # save page

    # save pdf
    c.save()
    #get the value of BytesIO buffer and write response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


