"""monolito URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pfimapp import views
from django.contrib.auth.views import LoginView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('usuarios/editar/<int:pk>/', views.CustomUserUpdateView.as_view(), name='customuser_update'),
    path('matricula/<int:matricula_id>/', views.detalleMatricula, name='detalle_matricula'),
    path('reporteMatricula/', views.reporteMatricula, name='reporteMatricula'),  
    path('reporteAcademico/', views.reporteAcademico, name='reporteAcademico'),  
    path('reporteEconomico/', views.reporteEconomico, name='reporteEconomico'),  
    path('logout/', views.signout, name='logount'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('signin/', LoginView.as_view(template_name='signin.html'), name='signin'),

    path('generar-pdf/', views.generar_pdf, name='generar-pdf'),

    path('accounts/profile/', RedirectView.as_view(url='/', permanent=False)),
]
