# Generated by Django 5.0.6 on 2024-05-16 20:53

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arrendatario',
            fields=[
                ('rut_arrendatario', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=12)),
                ('correo', models.CharField(max_length=200)),
                ('fecha_creacion', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('rut_cliente', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=12)),
                ('correo', models.CharField(max_length=200)),
                ('fecha_creacion', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Historial_propiedad',
            fields=[
                ('id_propiedad', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre_propietario', models.CharField(max_length=100)),
                ('fecha_venta', models.DateField()),
                ('antiguo_propietario', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Historial_venta',
            fields=[
                ('id_venta', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre_propietario', models.CharField(max_length=100)),
                ('fecha_venta', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Operacion_venta',
            fields=[
                ('id_op_venta', models.IntegerField(primary_key=True, serialize=False)),
                ('total_pago', models.IntegerField()),
                ('anticipo_pago', models.IntegerField()),
                ('fecha_pago', models.DateField()),
                ('comision', models.IntegerField()),
                ('bienes_raices', models.CharField(max_length=150)),
                ('propietario_actual', models.CharField(max_length=150)),
                ('propietario_nuevo', models.CharField(max_length=150)),
                ('fecha_inscripcion', models.DateField()),
                ('foja', models.FileField(upload_to='')),
                ('nombre_abogado', models.CharField(max_length=150)),
                ('correo_abogado', models.CharField(max_length=200)),
                ('telefono_abogado', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Propietario',
            fields=[
                ('rut_propietario', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=150)),
                ('telefono_1', models.CharField(max_length=12)),
                ('telefono_2', models.CharField(max_length=12)),
                ('correo', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaCorredora',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('rut_empresa', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nombre_empresa', models.CharField(default='', max_length=100)),
                ('telefono', models.CharField(max_length=15)),
                ('razon_social', models.CharField(max_length=100)),
                ('giro', models.CharField(max_length=100)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Agente',
            fields=[
                ('rut_agente', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=12)),
                ('correo', models.CharField(max_length=200)),
                ('fecha_creacion', models.DateField()),
                ('rut_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comprador',
            fields=[
                ('rut_comprador', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=12)),
                ('correo', models.CharField(max_length=200)),
                ('fecha_creacion', models.DateField()),
                ('rut_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Cuenta_bancaria',
            fields=[
                ('id_cuenta', models.IntegerField(primary_key=True, serialize=False)),
                ('alias', models.CharField(max_length=50)),
                ('banco', models.CharField(max_length=50)),
                ('tipo_cuenta', models.CharField(max_length=50)),
                ('nro_cuenta', models.IntegerField()),
                ('monto_cuenta', models.IntegerField()),
                ('rut_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Egreso_bancario',
            fields=[
                ('id_egreso', models.IntegerField(primary_key=True, serialize=False)),
                ('fecha_egreso', models.DateField()),
                ('egreso', models.IntegerField()),
                ('tipo_egreso', models.CharField(max_length=150)),
                ('id_cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cuenta_bancaria')),
            ],
        ),
        migrations.CreateModel(
            name='Historial_arriendo',
            fields=[
                ('id_arriendo', models.IntegerField(primary_key=True, serialize=False)),
                ('fecha_arriendo', models.DateField()),
                ('valor', models.IntegerField()),
                ('fecha', models.DateField()),
                ('nombre_arrendatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.arrendatario')),
            ],
        ),
        migrations.CreateModel(
            name='Cierre_Operacion',
            fields=[
                ('id_cierre', models.IntegerField(primary_key=True, serialize=False)),
                ('voucher', models.FileField(upload_to='')),
                ('escritura_propiedad', models.FileField(upload_to='')),
                ('rut_comprador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.comprador')),
                ('id_venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.historial_venta')),
            ],
        ),
        migrations.CreateModel(
            name='Ingreso_bancario',
            fields=[
                ('id_ingreso', models.IntegerField(primary_key=True, serialize=False)),
                ('fecha_ingreso', models.DateField()),
                ('monto_ingreso', models.IntegerField()),
                ('tipo_ingreso', models.CharField(max_length=150)),
                ('id_cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cuenta_bancaria')),
            ],
        ),
        migrations.CreateModel(
            name='Planes',
            fields=[
                ('id_planes', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre_plan', models.CharField(max_length=100)),
                ('valor_plan', models.IntegerField()),
                ('tipo_plan', models.CharField(max_length=20)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_termino', models.DateField()),
                ('capacidad_propiedades', models.IntegerField()),
                ('rut_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='planes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.planes'),
        ),
        migrations.CreateModel(
            name='Propiedad',
            fields=[
                ('id_propiedad', models.IntegerField(primary_key=True, serialize=False)),
                ('numero_rol', models.IntegerField()),
                ('tipo_propiedad', models.CharField(max_length=50)),
                ('tipo_operacion', models.CharField(max_length=50)),
                ('titulo', models.CharField(max_length=50)),
                ('estado', models.BooleanField()),
                ('descripcion_propiedad', models.TextField(blank=True, default='', null=True)),
                ('metros_cuadrados', models.IntegerField()),
                ('nro_habitaciones', models.IntegerField()),
                ('nro_bannos', models.IntegerField()),
                ('precio_tasacion', models.IntegerField()),
                ('direccion_propiedad', models.CharField(max_length=100)),
                ('rut_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id_contrato', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_firma', models.DateField()),
                ('estado', models.CharField(max_length=50)),
                ('tipo_contrato', models.CharField(max_length=50)),
                ('nro_propidades', models.IntegerField()),
                ('fecha_termino', models.DateField()),
                ('descripcion', models.TextField()),
                ('rut_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('rut_propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.propietario')),
            ],
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id_publicacion', models.IntegerField(primary_key=True, serialize=False)),
                ('tipo_moneda', models.CharField(max_length=10)),
                ('valor_tasacion', models.IntegerField()),
                ('precio', models.IntegerField()),
                ('iva', models.FloatField()),
                ('porctje_comision', models.FloatField()),
                ('monto_comision', models.IntegerField()),
                ('es_destacado', models.BooleanField()),
                ('id_propiedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.propiedad')),
                ('rut_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Operacion_arriendo',
            fields=[
                ('id_op_arriendo', models.IntegerField(primary_key=True, serialize=False)),
                ('fecha_contrato', models.DateField()),
                ('anticipo_arriendo', models.IntegerField()),
                ('valor_referencial', models.IntegerField()),
                ('fecha_publicacion', models.DateField()),
                ('arrendatario_actual', models.CharField(max_length=150)),
                ('id_arriendo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.historial_arriendo')),
                ('nombre_agente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.agente')),
                ('rut_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cliente')),
                ('nombre_propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.propietario')),
                ('id_publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.publicacion')),
            ],
        ),
    ]
