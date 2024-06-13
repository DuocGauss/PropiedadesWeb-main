from django.shortcuts import render
from .forms import frmRegistro, frmLogin, frmCliente, frmClienteEdit, frmTipoCliente, frmCrearPropiedad, frmActualizarPropiedad, frmContrato, frmPropietario, frmAgente, frmAgenteEdit
from .models import Cliente, Propiedad, Contrato, Propietario, Agente
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
    form_tipo_cliente = frmTipoCliente()
    empresa = request.user
    clientes = Cliente.objects.filter(empresa=empresa).order_by('-fecha_creacion')
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
    contexto["form_tipo_cliente"] = form_tipo_cliente
    contexto["clientes"] = clientes
    
    return render(request, 'core/clientes.html', contexto)


def cliente_create(request):
    if request.method == 'POST':
        form = frmCliente(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['rut']
            cliente = form.save(commit=False)  # Crear el objeto Cliente sin guardarlo aún 
            empresa = request.user
            if Cliente.objects.filter(rut=rut, empresa=empresa).exists():
                return JsonResponse({'error': 'El cliente ya existe en esta empresa'}, status=400)
            else:
                cliente.empresa = empresa
                form.save()
            return JsonResponse({'message': 'Cliente agregado correctamente'})
    return JsonResponse({'error': 'Formulario no válido'})


def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = frmClienteEdit(request.POST, instance=cliente)
        if form.is_valid():
            rut = form.cleaned_data['rut']
            empresa = request.user
            if Cliente.objects.filter(rut=rut, empresa=empresa).exclude(pk=pk).exists():
                return JsonResponse({'error': 'El cliente ya existe en esta empresa'}, status=400)
            else:
                form.save()
                return JsonResponse({'message': 'Cliente actualizado correctamente'})
    return JsonResponse({'error': 'Formulario no válido'})


def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
        return JsonResponse({'message': 'Cliente eliminado correctamente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)




@login_required
def add_tipo_cliente(request):
    if request.method == 'POST':
        form = frmTipoCliente(request.POST)
        if form.is_valid():
            cliente_id = request.POST.get('cliente_id')
            cliente = get_object_or_404(Cliente, id=cliente_id)
            tipo_cliente = form.save(commit=False)
            tipo_cliente.cliente = cliente
            tipo_cliente.save()
            return JsonResponse({'message': 'Tipo de cliente agregado correctamente'})
    return JsonResponse({'error': 'Formulario no válido'}, status=400)



@login_required
def listar_propiedades(request):
    rut_empresa = request.user
    propiedades = Propiedad.objects.filter(rut_empresa=rut_empresa).order_by('-id')
    agentes = Agente.objects.filter(rut_empresa=rut_empresa)
    contexto = {}
    form = frmCrearPropiedad(user=request.user)

    default_page = 1
    page = request.GET.get('page', default_page)
    query = request.GET.get('q')

    if query:
        propiedades = propiedades.filter(
            Q(numero_rol__icontains=query) |
            Q(tipo_propiedad__icontains=query) |
            Q(tipo_operacion__icontains=query) |
            Q(metros_cuadrados__icontains=query) |
            Q(precio_tasacion__icontains=query)
        )

    items_per_page = 5
    paginator = Paginator(propiedades, items_per_page)

    try:
        propiedades = paginator.page(page)
    except PageNotAnInteger:
        propiedades = paginator.page(default_page)
    except EmptyPage:
        propiedades = paginator.page(paginator.num_pages)

    contexto["propiedades"] = propiedades
    contexto["form"] = form
    contexto["agentes"] = agentes
    return render(request, 'core/propiedades.html', contexto)


def crear_propiedad(request):
    if request.method == 'POST':
        form = frmCrearPropiedad(request.POST, request.FILES)
        if form.is_valid():
            propiedad = form.save(commit=False)
            propiedad.rut_empresa = request.user
            form.save()
            return JsonResponse({'message': 'Propiedad agregada correctamente'})
    else:
        form = frmCrearPropiedad()
    return render(request, 'core/propiedades.html', {'form': form})


def actualizar_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    if request.method == 'POST':
        form = frmActualizarPropiedad(request.POST, request.FILES, instance=propiedad)
        if form.is_valid():
            estado = request.POST.get('estado') == 'true'
            propiedad.estado = estado
            form.save()
            return JsonResponse({'message': 'Propiedad actualizada correctamente'})
    return JsonResponse({'error': 'Formulario no válido'})
    

@login_required
def eliminar_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    if request.method == 'POST':
        propiedad.delete()
        return JsonResponse({'message': 'Propiedad eliminada correctamente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required
def publicacion(request):
    return render(request, 'core/publicacion.html')

@login_required
def op_venta(request):
    return render(request, 'core/op_venta.html')

@login_required
def op_arriendo(request):
    return render(request, 'core/op_arriendo.html')

@login_required
def propietarios(request):
    form = frmContrato()
    contratos = Contrato.objects.filter(rut_empresa=request.user).order_by('-fecha_firma')
    propietarios = Propietario.objects.filter(contrato__rut_empresa=request.user).distinct()
    contexto = {}
    default_page = 1
    page = request.GET.get('page', default_page)
    query = request.GET.get('q')

    if query:
        propietarios = propietarios.filter(
            Q(rut_propietario__icontains=query) |
            Q(nombre__icontains=query) |
            Q(telefono_1__icontains=query) |
            Q(telefono_2__icontains=query) |
            Q(correo__icontains=query)
        )

    items_per_page = 5
    paginator = Paginator(propietarios, items_per_page)

    try:
        propietarios = paginator.page(page)
    except PageNotAnInteger:
        propietarios = paginator.page(default_page)
    except EmptyPage:
        propietarios = paginator.page(paginator.num_pages)
    
    contexto["contratos"] = contratos
    contexto["propietarios"] = propietarios
    contexto["form"] = form
    
    return render(request, 'core/propietarios.html', contexto)

@login_required
def crear_nuevo_contrato(request):
    if request.method == 'POST':
        form = frmContrato(request.POST)
        if form.is_valid():
            contrato = form.save(commit=False)
            rut_empresa = request.user
            contrato.rut_empresa = rut_empresa

            rut_propietario_rut = request.POST.get('rut_propietario')
            rut_propietario = Propietario.objects.filter(
                rut_propietario=rut_propietario_rut,
                contrato__rut_empresa=rut_empresa
            ).distinct().first()

            if not rut_propietario:
                return JsonResponse({'error': 'Propietario no encontrado para esta empresa'})

            contrato.rut_propietario = rut_propietario
            contrato.save()

            return JsonResponse({'message': 'Contrato agregado correctamente'})
        else:
            return JsonResponse({'error': 'Formulario no válido'})

    return JsonResponse({'error': 'Método no permitido'})


@login_required
def crear_contrato(request):
    if request.method == 'POST':
        propietario_form = frmPropietario(request.POST)
        contrato_form = frmContrato(request.POST)
        if propietario_form.is_valid() and contrato_form.is_valid():
            rut_propietario = propietario_form.cleaned_data['rut_propietario']
            rut_empresa = request.user

            # Verificar si ya existe un propietario con el mismo rut_propietario para la empresa actual a través de contratos
            propietario = Propietario.objects.filter(
                rut_propietario=rut_propietario,
                contrato__rut_empresa=rut_empresa
            ).distinct().first()

            if propietario is None:
                propietario = propietario_form.save()

            contrato = contrato_form.save(commit=False)
            contrato.rut_propietario = propietario
            contrato.rut_empresa = rut_empresa  # Asignar la empresa corredora autenticada
            contrato.save()
            messages.success(request, "Propietario agregado")
            return redirect('propietarios')
    else:
        propietario_form = frmPropietario()
        contrato_form = frmContrato()
    return render(request, 'core/crear_contrato.html', {
        'propietario_form': propietario_form,
        'contrato_form': contrato_form
    })

    



@login_required
def eliminar_propietario(request, pk):
    propietario = get_object_or_404(Propietario, pk=pk)
    if request.method == 'POST':
        propietario.delete()
        return JsonResponse({'message': 'Propietario eliminado correctamente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required
def editar_propietario(request, pk):
    propietario = get_object_or_404(Propietario, pk=pk)
    if request.method == 'POST':
        form = frmPropietario(request.POST, instance=propietario)
        if form.is_valid():
            nuevo_rut_propietario = form.cleaned_data['rut_propietario']
            empresa = request.user
            # Verificar si el nuevo RUT ya existe para la misma empresa, excluyendo el propietario actual
            if Propietario.objects.filter(rut_propietario=nuevo_rut_propietario, contrato__rut_empresa=empresa).exclude(pk=pk).exists():
                return JsonResponse({'error': 'El propietario ya existe en esta empresa'}, status=400)
            else:
                form.save()
                return JsonResponse({'message': 'Propietario actualizado correctamente'})
    return JsonResponse({'error': 'Formulario no válido'}, status=400)


@login_required
def agentes(request):
    form = frmAgente()
    empresa = request.user
    agentes = Agente.objects.filter(rut_empresa=empresa).order_by('-fecha_creacion')
    contexto = {}
    
    default_page = 1
    page = request.GET.get('page', default_page)
    query = request.GET.get('q')
    
    if query:
        # Filtrar mantenciones en función de la búsqueda
        agentes = agentes.filter(
            Q(rut_agente__icontains=query) |
            Q(nombre__icontains=query) |
            Q(direccion__icontains=query) |
            Q(telefono__icontains=query) |
            Q(correo__icontains=query)  
        )

    items_per_page = 5  # Ajusta el número de elementos por página según tus necesidades
    paginator = Paginator(agentes, items_per_page)

    try:
        agentes = paginator.page(page)
    except PageNotAnInteger:
        agentes = paginator.page(default_page)
    except EmptyPage:
        agentes = paginator.page(paginator.num_pages)
        
    contexto["form"] = form
    contexto["agentes"] = agentes
    return render(request, 'core/agentes.html', contexto)


def crear_agente(request):
    if request.method == 'POST':
        form = frmAgente(request.POST)
        if form.is_valid():
            rut_agente = form.cleaned_data['rut_agente']
            agente = form.save(commit=False)  # Crear el objeto Cliente sin guardarlo aún 
            empresa = request.user
            if Agente.objects.filter(rut_agente=rut_agente, rut_empresa=empresa).exists():
                return JsonResponse({'error': 'El agente ya existe en esta empresa'}, status=400)
            else:
                agente.rut_empresa = empresa
                form.save()
            return JsonResponse({'message': 'Agente agregado correctamente'})
    return JsonResponse({'error': 'Formulario no válido'})


def editar_agente(request, pk):
    agente = get_object_or_404(Agente, pk=pk)
    if request.method == 'POST':
        form = frmAgenteEdit(request.POST, instance=agente)
        if form.is_valid():
            rut_agente = form.cleaned_data['rut_agente']
            empresa = request.user
            if Agente.objects.filter(rut_agente=rut_agente, rut_empresa=empresa).exclude(pk=pk).exists():
                return JsonResponse({'error': 'El agente ya existe en esta empresa'}, status=400)
            else:
                form.save()
                return JsonResponse({'message': 'Agente actualizado correctamente'})
    return JsonResponse({'error': 'Formulario no válido'})


def eliminar_agente(request, pk):
    agente = get_object_or_404(Agente, pk=pk)
    if request.method == "POST":
        agente.delete()
        return JsonResponse({'message': 'Agente eliminado correctamente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def detalles_publicacion(request):
    return render(request, 'core/detalles_publicacion.html')


def planes(request):
    return render(request, 'core/planes.html')