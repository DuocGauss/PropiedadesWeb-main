from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.deletion import CASCADE

# Ejemplo de establecer un límite mínimo y máximo para el campo integer
#    mi_entero = models.IntegerField(
#        validators=[
#            MinValueValidator(0),  # Establece el límite mínimo, por ejemplo, 0
#            MaxValueValidator(100) # Establece el límite máximo, por ejemplo, 100
#        ]
#    )

# Create your models here.


class EmpresaCorredora(AbstractUser):
    rut_empresa = models.CharField(max_length=50, primary_key=True)
    nombre_empresa = models.CharField(default="", max_length=100)
    telefono = models.CharField(max_length=15)
    razon_social = models.CharField(max_length=100)
    giro = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.rut_empresa} - {self.username}"

class Agente(models.Model):
    rut_agente = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=12)
    correo = models.CharField(max_length=200)
    fecha_creacion = models.DateField()
    rut_empresa = models.ForeignKey(EmpresaCorredora, on_delete= CASCADE)

    def __str__(self):
        return f"{self.rut_agente} - {self.nombre}"
    
class Arrendatario(models.Model):
    rut_arrendatario = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=12)
    correo = models.CharField(max_length=200)
    fecha_creacion = models.DateField()

    def __str__(self):
        return f"{self.rut_arrendatario} - {self.nombre}"
    
class Planes(models.Model):
    id_planes = models.IntegerField(primary_key=True)
    nombre_plan = models.CharField(max_length=100)
    valor_plan = models.IntegerField()
    tipo_plan = models.CharField(max_length=20)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    capacidad_propiedades = models.IntegerField()
    rut_empresa = models.ForeignKey(EmpresaCorredora, on_delete=CASCADE)

    def __str__(self):
        return f"{self.id_planes}"
    
class Cliente(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=12)
    correo = models.CharField(max_length=200)
    fecha_creacion = models.DateField()

    def __str__(self):
        return f"{self.rut} - {self.nombre}"
    
class Tipo_Cliente(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    tipo_cliente = models.CharField(max_length=50)
    rut_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_tipo} - {self.tipo_cliente}"
    
class Comprador(models.Model):
    rut_comprador = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=12)
    correo = models.CharField(max_length=200)
    fecha_creacion = models.DateField()
    rut_cliente = models.ForeignKey(Cliente, on_delete=CASCADE)

    def __str__(self):
        return f"{self.rut_comprador} - {self.nombre}"
    
class Propietario(models.Model):
    rut_propietario = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=150)
    telefono_1 = models.CharField(max_length=12)
    telefono_2 = models.CharField(max_length=12)
    correo = models.CharField(max_length=200)  

    def __str__(self):
        return f"{self.rut_propietario} - {self.nombre}"

class Contrato(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    fecha_firma = models.DateField()
    estado = models.CharField(max_length=50)
    tipo_contrato = models.CharField(max_length=50)
    nro_propidades = models.IntegerField()
    fecha_termino = models.DateField()
    descripcion = models.TextField()
    rut_propietario = models.ForeignKey(Propietario, on_delete=CASCADE)
    rut_empresa = models.ForeignKey(EmpresaCorredora, on_delete=CASCADE)

    def __str__(self):
        return f"{self.id_contrato}"
    
class Cuenta_bancaria(models.Model):
    id_cuenta = models.IntegerField(primary_key=True)
    alias = models.CharField(max_length=50)
    banco = models.CharField(max_length=50)
    tipo_cuenta = models.CharField(max_length=50)
    nro_cuenta = models.IntegerField()
    monto_cuenta = models.IntegerField()
    rut_empresa = models.ForeignKey(EmpresaCorredora, on_delete=CASCADE)

    def __str__(self):
        return f"{self.id_cuenta}"
    
class Egreso_bancario(models.Model):
    id_egreso = models.IntegerField(primary_key=True)
    fecha_egreso = models.DateField()
    egreso = models.IntegerField()
    tipo_egreso = models.CharField(max_length=150)
    id_cuenta = models.ForeignKey(Cuenta_bancaria, on_delete=CASCADE)

    def __str__(self):
        return f"{self.id_egreso}"
    
class Ingreso_bancario(models.Model):
    id_ingreso = models.IntegerField(primary_key=True)
    fecha_ingreso = models.DateField()
    monto_ingreso = models.IntegerField()
    tipo_ingreso = models.CharField(max_length=150)
    id_cuenta = models.ForeignKey(Cuenta_bancaria, on_delete=CASCADE)

    def __str__(self):
        return f"{self.id_ingreso}" 
    
class Historial_arriendo(models.Model):
    id_arriendo = models.IntegerField(primary_key=True)
    fecha_arriendo = models.DateField()
    valor = models.IntegerField()
    fecha = models.DateField()
    nombre_arrendatario = models.ForeignKey(Arrendatario, on_delete=CASCADE)

    def __str__(self):
        return f"{self.id_arriendo}"
    
class Historial_propiedad(models.Model):
    id_propiedad = models.IntegerField(primary_key=True)
    nombre_propietario = models.CharField(max_length=100)
    fecha_venta = models.DateField()
    antiguo_propietario = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id_propiedad}"
    
class Historial_venta(models.Model):
    id_venta = models.IntegerField(primary_key=True)
    nombre_propietario = models.CharField(max_length=100)
    fecha_venta = models.DateField()

    def __str__(self):
        return f"{self.id_venta}"

class Cierre_Operacion(models.Model):
    id_cierre = models.IntegerField(primary_key=True)
    voucher = models.FileField()
    escritura_propiedad = models.FileField()
    id_venta = models.ForeignKey(Historial_venta, on_delete= CASCADE)
    rut_comprador = models.ForeignKey(Comprador, on_delete=CASCADE)

    def __str__(self):
        return f"{self.id_cierre}"
    
class Propiedad(models.Model):
    id_propiedad = models.IntegerField(primary_key=True)
    numero_rol = models.IntegerField()
    tipo_propiedad = models.CharField(max_length=50)
    tipo_operacion = models.CharField(max_length=50)
    titulo = models.CharField(max_length=50)
    estado = models.BooleanField()
    descripcion_propiedad = models.TextField(default="", null=True, blank=True)
    metros_cuadrados = models.IntegerField()
    nro_habitaciones = models.IntegerField()
    nro_bannos = models.IntegerField()
    precio_tasacion = models.IntegerField()
    direccion_propiedad = models.CharField(max_length=100)
    rut_empresa = models.ForeignKey(EmpresaCorredora, on_delete=CASCADE)
    

    def __str__(self):
        return f"{self.id_propiedad}"
        
class Publicacion(models.Model):
    id_publicacion = models.IntegerField(primary_key=True)
    tipo_moneda = models.CharField(max_length=10)
    valor_tasacion = models.IntegerField()
    precio = models.IntegerField()
    iva = models.FloatField()
    porctje_comision = models.FloatField()
    monto_comision = models.IntegerField()
    es_destacado = models.BooleanField()
    rut_cliente = models.ForeignKey(Cliente, on_delete=CASCADE)
    id_propiedad = models.ForeignKey(Propiedad, on_delete=CASCADE)

    def __str__(self):
        return f"{self.id_publicacion}"
    
class Operacion_arriendo(models.Model):
    id_op_arriendo = models.IntegerField(primary_key=True)
    fecha_contrato = models.DateField()
    anticipo_arriendo = models.IntegerField()
    valor_referencial = models.IntegerField()
    fecha_publicacion = models.DateField()
    arrendatario_actual = models.CharField(max_length=150)
    rut_cliente = models.ForeignKey(Cliente, on_delete=CASCADE)
    id_arriendo = models.ForeignKey(Historial_arriendo, on_delete=CASCADE)
    id_publicacion = models.ForeignKey(Publicacion, on_delete=CASCADE)
    nombre_propietario = models.ForeignKey(Propietario, on_delete=CASCADE)
    nombre_agente = models.ForeignKey(Agente, on_delete=CASCADE)

    def __str__(self):
        return f"{self.id_op_arriendo}"
    
class Operacion_venta(models.Model):
    id_op_venta = models.IntegerField(primary_key=True)
    total_pago = models.IntegerField()
    anticipo_pago = models.IntegerField()
    fecha_pago = models.DateField()
    comision = models.IntegerField()
    #conservador de bienes y raices
    bienes_raices = models.CharField(max_length=150)
    propietario_actual = models.CharField(max_length=150)
    propietario_nuevo = models.CharField(max_length=150)
    fecha_inscripcion = models.DateField()
    foja = models.FileField()
    nombre_abogado = models.CharField(max_length=150)
    correo_abogado = models.CharField(max_length=200)
    telefono_abogado = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.id_op_venta}"
    