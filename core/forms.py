from django import forms
from .models import EmpresaCorredora, Cliente
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
        
            
        