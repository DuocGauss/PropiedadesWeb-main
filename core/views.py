from django.shortcuts import render
from .forms import frmRegistro, frmLogin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout

# Create your views here.

def home(request):
    return render(request, 'core/home.html')



def registro(request):
    if request.method == 'POST':
        form = frmRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            user.save()
            messages.success(request,"Cuenta creada!")
            return redirect('home')  # Redirigir a la página de inicio después del registro
    else:
        form = frmRegistro()
    
    contexto = {
        'form': form,
    }
        
    return render(request, 'registration/registro.html', contexto)



def iniciar_sesion(request):
    if request.method == 'POST':
        form = frmLogin(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirigir a la página de inicio después de iniciar sesión
    else:
        form = frmLogin()
    
    return render(request, 'registration/iniciar_sesion.html', {'form': form})


def cerrar_sesion(request):
    logout(request)
    return redirect('home')