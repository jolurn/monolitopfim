# Generated by Django 4.1.7 on 2023-04-12 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(error_messages={'unique': 'Este correo electrónico ya está en uso.'}, max_length=100, unique=True)),
                ('nacionalidad', models.CharField(max_length=100)),
                ('numeroDocumento', models.CharField(error_messages={'unique': 'Este DNI ya está en uso.'}, max_length=100, unique=True)),
                ('numeroUbigeoNacimiento', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=200)),
                ('codigoEgresadoUNI', models.CharField(blank=True, max_length=20, null=True)),
                ('primerNombre', models.CharField(max_length=100)),
                ('segundoNombre', models.CharField(blank=True, max_length=100, null=True)),
                ('apellidoPaterno', models.CharField(max_length=100)),
                ('apellidoMaterno', models.CharField(max_length=100)),
                ('correoUNI', models.CharField(blank=True, max_length=100, null=True)),
                ('gradoEstudio', models.CharField(max_length=200)),
                ('universidadProcedencia', models.CharField(max_length=200)),
                ('telefono', models.CharField(max_length=15)),
                ('fechaNacimiento', models.DateField(blank=True, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigoUniPreGrado', models.CharField(blank=True, max_length=10, null=True)),
                ('codigoAlumPFIM', models.CharField(blank=True, max_length=15, null=True)),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
                ('ipUsuario', models.CharField(blank=True, default='192.168.0.101', max_length=100, null=True)),
                ('usuarioPosgradoFIM', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Alumnos',
            },
        ),
        migrations.CreateModel(
            name='ConceptoPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
                ('ipUsuario', models.CharField(blank=True, default='192.168.0.101', max_length=100, null=True)),
                ('usuarioPosgradoFIM', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Conceptos de Pagos',
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=10)),
                ('nombre', models.CharField(max_length=100)),
                ('credito', models.IntegerField()),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
                ('ipUsuario', models.CharField(blank=True, default='192.168.0.101', max_length=100, null=True)),
                ('usuarioPosgradoFIM', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Cursos',
            },
        ),
        migrations.CreateModel(
            name='DetalleMatricula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promedioFinal', models.FloatField(blank=True, null=True)),
                ('retirado', models.BooleanField(default=False)),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
                ('ipUsuario', models.CharField(blank=True, default='192.168.0.101', max_length=100, null=True)),
                ('usuarioPosgradoFIM', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Detalle de Matriculas',
            },
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
                ('ipUsuario', models.CharField(blank=True, default='192.168.0.101', max_length=100, null=True)),
                ('usuarioPosgradoFIM', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Docentes',
            },
        ),
        migrations.CreateModel(
            name='EstadoAcademico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
                ('ipUsuario', models.CharField(blank=True, default='192.168.0.101', max_length=100, null=True)),
                ('usuarioPosgradoFIM', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Estados Academico',
            },
        ),
        migrations.CreateModel(
            name='EstadoBoletaP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
                ('ipUsuario', models.CharField(blank=True, default='192.168.0.101', max_length=100, null=True)),
                ('usuarioPosgradoFIM', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Estados Boletas Pagos',
            },
        ),
        migrations.CreateModel(
            name='EstadoCivil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
                ('ipUsuario', models.CharField(blank=True, default='192.168.0.101', max_length=100, null=True)),
                ('usuarioPosgradoFIM', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Estado Civil',
            },
        ),
        migrations.CreateModel(
            name='Maestria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=10)),
                ('nombre', models.CharField(max_length=100)),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
                ('ipUsuario', models.CharField(blank=True, default='192.168.0.101', max_length=100, null=True)),
                ('usuarioPosgradoFIM', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Maestrias',
            },
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=100)),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
                ('ipUsuario', models.CharField(blank=True, default='192.168.0.101', max_length=100, null=True)),
                ('usuarioPosgradoFIM', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Periodos',
            },
        ),
        migrations.CreateModel(
            name='ReporteEcoConceptoPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.FloatField()),
                ('numeroRecibo', models.CharField(blank=True, max_length=100, null=True)),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
                ('ipUsuario', models.CharField(blank=True, default='192.168.0.101', max_length=100, null=True)),
                ('usuarioPosgradoFIM', models.CharField(blank=True, max_length=200, null=True)),
                ('conceptoPago', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.conceptopago')),
                ('estadoBoletaPago', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.estadoboletap')),
                ('periodo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.periodo')),
            ],
        ),
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
                ('ipUsuario', models.CharField(blank=True, default='192.168.0.101', max_length=100, null=True)),
                ('usuarioPosgradoFIM', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Sede',
            },
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
                ('ipUsuario', models.CharField(blank=True, default='192.168.0.101', max_length=100, null=True)),
                ('usuarioPosgradoFIM', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Tipo de Documentos',
            },
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aulaWeb', models.CharField(blank=True, max_length=100, null=True)),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
                ('ipUsuario', models.CharField(blank=True, default='192.168.0.101', max_length=100, null=True)),
                ('usuarioPosgradoFIM', models.CharField(blank=True, max_length=200, null=True)),
                ('curso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.curso')),
                ('docente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.docente')),
                ('maestria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.maestria')),
                ('periodo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.periodo')),
            ],
            options={
                'verbose_name_plural': 'Secciones',
            },
        ),
        migrations.CreateModel(
            name='ReporteEconomico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
                ('ipUsuario', models.CharField(blank=True, default='192.168.0.101', max_length=100, null=True)),
                ('usuarioPosgradoFIM', models.CharField(blank=True, max_length=200, null=True)),
                ('alumno', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.alumno')),
                ('conceptoPago', models.ManyToManyField(blank=True, through='pfimapp.ReporteEcoConceptoPago', to='pfimapp.conceptopago')),
            ],
            options={
                'verbose_name_plural': 'Reportes Economicos',
            },
        ),
        migrations.AddField(
            model_name='reporteecoconceptopago',
            name='reporteEconomico',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.reporteeconomico'),
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A', max_length=1)),
                ('fechaRegistro', models.DateField(default=django.utils.timezone.now)),
                ('fechaModificado', models.DateField(auto_now=True, null=True)),
                ('ipUsuario', models.CharField(blank=True, default='192.168.0.101', max_length=100, null=True)),
                ('usuarioPosgradoFIM', models.CharField(blank=True, max_length=200, null=True)),
                ('alumno', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.alumno')),
                ('periodo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.periodo')),
                ('seccion', models.ManyToManyField(blank=True, through='pfimapp.DetalleMatricula', to='pfimapp.seccion')),
            ],
            options={
                'verbose_name_plural': 'Matriculas',
            },
        ),
        migrations.AddField(
            model_name='docente',
            name='maestria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.maestria'),
        ),
        migrations.AddField(
            model_name='docente',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='detallematricula',
            name='matricula',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.matricula'),
        ),
        migrations.AddField(
            model_name='detallematricula',
            name='seccion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.seccion'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='estadoAcademico',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.estadoacademico'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='maestria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.maestria'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='periodoDeIngreso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.periodo'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customuser',
            name='estadoCivil',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.estadocivil'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='maestria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.maestria'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='sede',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.sede'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='tipoDocumento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pfimapp.tipodocumento'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]