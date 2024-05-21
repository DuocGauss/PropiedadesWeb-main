from django.shortcuts import render
from .forms import frmRegistro, frmLogin, frmCliente, frmClienteEdit
from .models import Cliente
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View

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



@login_required
def cliente_list(request):
    form = frmCliente()
    clientes = Cliente.objects.all().order_by('-fecha_creacion')
    contexto = {}
    
    default_page = 1
    page = request.GET.get('page', default_page)
    query = request.GET.get('q')
    
    if query:
        # Filtrar mantenciones en función de la búsqueda
        clientes = clientes.filter(
            Q(rut__icontains=query) |
            Q(nombre__icontains=query) |
            Q(direccion__icontains=query) |
            Q(telefono__icontains=query) |
            Q(correo__icontains=query)  
        )

    items_per_page = 5  # Ajusta el número de elementos por página según tus necesidades
    paginator = Paginator(clientes, items_per_page)

    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        clientes = paginator.page(default_page)
    except EmptyPage:
        clientes = paginator.page(paginator.num_pages)
        
    contexto["form"] = form
    contexto["clientes"] = clientes
    
    return render(request, 'core/clientes.html', contexto)


def cliente_create(request):
    if request.method == 'POST':
        form = frmCliente(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Cliente agregado correctamente'})
    return JsonResponse({'error': 'Formulario no válido'})


def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = frmClienteEdit(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Cliente actualizado correctamente'})
    return JsonResponse({'error': 'Formulario no válido'})


def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
        return JsonResponse({'message': 'Cliente eliminado correctamente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


        
