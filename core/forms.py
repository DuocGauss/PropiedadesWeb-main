from django import forms
from .models import EmpresaCorredora, Cliente, Tipo_Cliente, Propiedad
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
            'descripcion_propiedad', 'metros_cuadrados', 'nro_habitaciones', 'nro_bannos',
            'direccion_propiedad',
        ]
    titulo = forms.FileField(required=False)
         

class frmActualizarPropiedad(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = [
           'numero_rol','tipo_propiedad', 'tipo_operacion', 'estado', 'precio_tasacion', 
           'descripcion_propiedad', 'metros_cuadrados', 'nro_habitaciones', 'nro_bannos',
           'direccion_propiedad',
        ]