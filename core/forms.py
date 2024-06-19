from django import forms
from .models import EmpresaCorredora, Cliente, Tipo_Cliente, Propiedad, Propietario, Contrato, Agente, Ubicacion, Publicacion
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm



class frmRegistro(UserCreationForm):
    class Meta:
        model = EmpresaCorredora
        fields = ['rut_empresa','username', 'email', 'telefono', 'password1', 'password2', 'razon_social', 'giro']
        
        
class frmLogin(AuthenticationForm):
    class Meta:
        model = EmpresaCorredora 
        fields = ['username', 'password'] 
        
        
class frmCliente(forms.ModelForm):
    class Meta:
        model=Cliente
        fields=["rut","nombre","direccion","telefono","correo","fecha_creacion"]
        widgets = {
            'fecha_creacion': forms.DateInput(attrs={'type': 'date'})
        } 
        

class frmClienteEdit(forms.ModelForm):
    class Meta:
        model=Cliente
        fields=["rut","nombre","direccion","telefono","correo"]
        
            
class frmTipoCliente(forms.ModelForm):
    class Meta:
        model=Tipo_Cliente
        fields=["tipo_cliente"]
        
        
        


class frmCrearPropiedad(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = [
            'numero_rol','tipo_propiedad', 'tipo_operacion', 'titulo', 'estado', 'precio_tasacion',
            'descripcion_propiedad', 'metros_cuadrados', 'nro_habitaciones', 'nro_bannos','rut_agente'
        ]
    titulo = forms.FileField(required=False)


class frmUbicacion(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['calle', 'num_calle', 'num_propiedad', 'comuna', 'region', 'google_maps_link']
    

class frmActualizarPropiedad(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = [
           'numero_rol','tipo_propiedad', 'tipo_operacion', 'estado', 'precio_tasacion', 
           'descripcion_propiedad', 'metros_cuadrados', 'nro_habitaciones', 'nro_bannos','rut_agente',
        ]

        
        
class frmPropietario(forms.ModelForm):
    class Meta:
        model = Propietario
        fields = ['rut_propietario','nombre', 'telefono_1','telefono_2', 'correo']
        



class frmContrato(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['fecha_firma','estado','tipo_contrato','nro_propidades','fecha_termino', 'descripcion']
        widgets = {
            'fecha_firma': forms.DateInput(attrs={'type': 'date'}),
            'fecha_termino': forms.DateInput(attrs={'type': 'date'})
        }
        


class frmAgente(forms.ModelForm):
    class Meta:
        model=Agente
        fields=["rut_agente","nombre","direccion","telefono","correo","fecha_creacion"]
        widgets = {
            'fecha_creacion': forms.DateInput(attrs={'type': 'date'})
        } 
        

class frmAgenteEdit(forms.ModelForm):
    class Meta:
        model=Agente
        fields=["rut_agente","nombre","direccion","telefono","correo"]
        
        
        


class frmPublicacion(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['tipo_moneda','valor_tasacion','precio','iva','porctje_comision','monto_comision','es_destacado']