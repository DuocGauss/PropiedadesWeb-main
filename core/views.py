from django.shortcuts import render
from .forms import frmRegistro, frmLogin, frmCliente, frmClienteEdit, frmTipoCliente, frmCrearPropiedad, frmActualizarPropiedad, frmContrato, frmPropietario, frmAgente, frmAgenteEdit, frmUbicacion, frmPublicacion
from .models import Cliente, Propiedad, Contrato, Propietario, Agente, Publicacion, Imagen
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views import View
from django.views.decorators.http import require_POST

# Create your views here.

def home(request):
    publicaciones = Publicacion.objects.all()
    return render(request, 'core/home.html', {'publicaciones': publicaciones})



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
    contexto = {}
    form = frmCrearPropiedad()

    default_page = 1
    page = request.GET.get('page', default_page)
    query = request.GET.get('q')

    if query:
        propiedades = propiedades.filter(
            Q(numero_rol__icontains=query) |
            Q(tipo_propiedad__icontains=query) |
            Q(tipo_operacion__icontains=query) |
            Q(ubicacion__comuna__icontains=query) |
            Q(ubicacion__region__icontains=query) |
            Q(ubicacion__calle__icontains=query) |
            Q(ubicacion__num_calle__icontains=query) |
            Q(ubicacion__num_propiedad__icontains=query) |
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
    return render(request, 'core/propiedades.html', contexto)


@login_required
def crear_propiedad(request):
    if request.method == 'POST':
        propiedad_form = frmCrearPropiedad(request.POST, request.FILES)
        ubicacion_form = frmUbicacion(request.POST)
        if propiedad_form.is_valid() and ubicacion_form.is_valid():
            ubicacion = ubicacion_form.save()
            propiedad = propiedad_form.save(commit=False)
            propiedad.ubicacion = ubicacion
            propiedad.rut_empresa = request.user
            propiedad.save()
            messages.success(request, "Propiedad agregada correctamente")
            return redirect('imagen', propiedad.id)
    else:
        propiedad_form = frmCrearPropiedad()
        ubicacion_form = frmUbicacion()
        
        # Filtrar agentes asociados al usuario autenticado
        propiedad_form.fields['rut_agente'].queryset = Agente.objects.filter(rut_empresa=request.user)
    
    return render(request, 'core/crear_propiedad.html', {
        'propiedad_form': propiedad_form,
        'ubicacion_form': ubicacion_form
    })
    
@login_required        
def imagen(request, propiedad_id):
    propiedad = Propiedad.objects.get(id=propiedad_id)
    imagenes = Imagen.objects.filter(propiedad=propiedad_id)
    
    # Verificar si la propiedad pertenece a la empresa del usuario autenticado
    if propiedad.rut_empresa != request.user:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")
    
    if request.method == 'POST':
        for file in request.FILES.getlist('file'):
            Imagen.objects.create(propiedad=propiedad, imagen=file)
        
        messages.success(request, "Datos guardados correctamente")
        return redirect('listar')
    return render(request, 'core/imagen.html', {'propiedad': propiedad, 'imagenes': imagenes})


@login_required
def editar_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    ubicacion = propiedad.ubicacion
    
    # Verificar si la propiedad pertenece a la empresa del usuario autenticado
    if propiedad.rut_empresa != request.user:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")

    if request.method == 'POST':
        propiedad_form = frmCrearPropiedad(request.POST, request.FILES, instance=propiedad)
        ubicacion_form = frmUbicacion(request.POST, instance=ubicacion)
        
        if propiedad_form.is_valid() and ubicacion_form.is_valid():
            ubicacion_form.save()
            propiedad_form.save()
            messages.success(request, "Propiedad actualizada correctamente")
            return redirect('listar')
    else:
        propiedad_form = frmCrearPropiedad(instance=propiedad)
        ubicacion_form = frmUbicacion(instance=ubicacion)
        
        # Filtrar agentes asociados al usuario autenticado
        propiedad_form.fields['rut_agente'].queryset = Agente.objects.filter(rut_empresa=request.user)
    
    return render(request, 'core/editar_propiedad.html', {
        'propiedad_form': propiedad_form,
        'ubicacion_form': ubicacion_form
    })
    

@require_POST
@login_required
def eliminar_imagen(request, id):
    imagen = get_object_or_404(Imagen, id=id)

    # Verificar que la imagen pertenece a la propiedad del usuario autenticado
    if imagen.propiedad.rut_empresa != request.user:
        return JsonResponse({'error': 'No tienes permiso para eliminar esta imagen'}, status=403)

    # Eliminar la imagen
    imagen.delete()

    return JsonResponse({'message': 'Imagen eliminada correctamente'})
    

@login_required
def eliminar_propiedad(request, pk):
    propiedad = get_object_or_404(Propiedad, pk=pk)
    if request.method == 'POST':
        propiedad.delete()
        return JsonResponse({'message': 'Propiedad eliminada correctamente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)





@login_required
def publicacion(request):
    rut_empresa = request.user
    propiedades = Propiedad.objects.filter(rut_empresa=rut_empresa)
    publicaciones = Publicacion.objects.filter(id_propiedad__in=propiedades)
    
    contexto = {}

    default_page = 1
    page = request.GET.get('page', default_page)
    query = request.GET.get('q')

    if query:
        publicaciones = publicaciones.filter(
            Q(id_propiedad__rut_agente__rut_agente__icontains=query) |
            Q(id_propiedad__rut_agente__nombre__icontains=query) |
            Q(tipo_moneda__icontains=query) |
            Q(valor_tasacion__icontains=query) |
            Q(precio__icontains=query) |
            Q(iva__icontains=query) |
            Q(porctje_comision__icontains=query) |
            Q(monto_comision__icontains=query) |
            Q(es_destacado__icontains=query) 
        )

    items_per_page = 5
    paginator = Paginator(publicaciones, items_per_page)

    try:
        publicaciones = paginator.page(page)
    except PageNotAnInteger:
        publicaciones = paginator.page(default_page)
    except EmptyPage:
        publicaciones = paginator.page(paginator.num_pages)

    contexto["publicaciones"] = publicaciones
    return render(request, 'core/publicacion.html', contexto)

@login_required
def crear_publicacion(request, propiedad_id):
    propiedad = Propiedad.objects.get(id=propiedad_id)
    # Verificar si la propiedad pertenece a la empresa del usuario autenticado
    if propiedad.rut_empresa != request.user:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")
    
    if request.method == 'POST':
        form = frmPublicacion(request.POST)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.id_propiedad = propiedad
            publicacion.save()
            messages.success(request, "Propiedad publicada correctamente")
            return redirect('publicacion')  # Redirige a una página de éxito
    else:
        form = frmPublicacion()
    
    return render(request, 'core/crear_publicacion.html', {'form': form})


@login_required
def editar_publicacion(request, id_publicacion):
    publicacion = get_object_or_404(Publicacion, id_publicacion=id_publicacion)
    
    # Verificar si la propiedad pertenece a la empresa del usuario autenticado
    if publicacion.id_propiedad.rut_empresa != request.user:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")

    if request.method == 'POST':
        form = frmPublicacion(request.POST, instance=publicacion)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Publicación actualizada correctamente")
            return redirect('publicacion')
    else:
        form = frmPublicacion(instance=publicacion)
    
    return render(request, 'core/editar_publicacion.html', {'form': form,})

@login_required
def eliminar_publicacion(request, id_publicacion):
    publicacion = get_object_or_404(Publicacion, id_publicacion=id_publicacion)
    if request.method == 'POST':
        publicacion.delete()
        return JsonResponse({'message': 'Publicación eliminada correctamente'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

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


def detalles_publicacion(request, id_publicacion):
    publicaciones = Publicacion.objects.filter(id_publicacion=id_publicacion)
    return render(request, 'core/detalles_publicacion.html', {'publicaciones': publicaciones})


def planes(request):
    return render(request, 'core/planes.html')