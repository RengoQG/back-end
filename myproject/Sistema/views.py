from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import CustomUser, RutaDeAutobus
from django.contrib.auth import authenticate, login
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import Ciudad 
from .models import AsociacionParadaRuta
# Asegúrate de importar tu modelo de Ciudad
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import HttpResponseRedirect
from .models import ParadaDeAutobus
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from .models import RutaDeAutobus  # Asegúrate de importar tu modelo de ruta
from django.views.decorators.csrf import csrf_exempt


def inicioSesion(request):
    return render(request, 'Sistema/login.html')

def custom_login(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Intenta autenticar en tu tabla personalizada
        try:
            custom_user = CustomUser.objects.get(username=username)
            if custom_user.check_password(password):
                login(request, custom_user)
                
                # Verifica el rol del usuario
                if custom_user.rol == 'logistico':
                    # Redirige a la vista del formulario de operador logístico
                    return redirect('/dash')
                else:
                    # Redirige a la vista del formulario para otros roles
                        return render(request, 'Sistema/pasajeros.html')
            else:
                error_message = "Nombre de usuario o contraseña incorrectos."
        except CustomUser.DoesNotExist:
            error_message = "Nombre de usuario o contraseña incorrectos."

    return render(request, 'Sistema/login.html', {'error_message': error_message})

def register(request):
    error_message = None
    success_message = None

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            rol = form.cleaned_data['rol']

            # Verifica si el nombre de usuario ya existe
            if CustomUser.objects.filter(username=username).exists():
                error_message = "El nombre de usuario ya está en uso."
            else:
                # Crear un nuevo usuario
                user = CustomUser(username=username, rol=rol)
                user.set_password(password)
                user.save()
                login(request, user)
                success_message = "Usuario registrado con éxito. Bienvenido."

        else:
            error_message = "No se pudo crear el usuario. Por favor, verifica los datos."

    else:
        form = CustomUserCreationForm()

    return render(request, 'Sistema/register.html', {'form': form, 'error_message': error_message, 'success_message': success_message})

#@login_required
@csrf_exempt
def datosCiudad(request):
    ciudades = Ciudad.objects.all()  
    message = None  

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')
        ciudad_id = request.POST.get('ciudad_id')

        if not nombre or not latitud or not longitud:
            message = "Por favor, complete todos los campos obligatorios."
        elif not latitud.isdigit() or not longitud.isdigit():
            message = "Las coordenadas deben ser valores numéricos."

        if not message:
            try:
                nueva_parada = ParadaDeAutobus(nombre=nombre, latitud=latitud, longitud=longitud, ciudad_id=ciudad_id)
                nueva_parada.save()
                message = "Parada registrada con éxito."
            except Exception as e:
                message = "Error al registrar la parada: " + str(e)

        # Verifica si la solicitud espera una respuesta JSON
        if 'application/json' in request.META.get('HTTP_ACCEPT'):
            # Construye una respuesta JSON
            response_data = {'message': message}
            return JsonResponse(response_data)
        else:
            # Respuesta HTML
            return render(request, 'Sistema/agregarParada.html', {'ciudades': ciudades, 'message': message})

    return render(request, 'Sistema/agregarParada.html', {'ciudades': ciudades, 'message': message})

def agregar_parada_a_ruta(request, ruta_id):
    error_message = None
    success_message = None
    ruta = get_object_or_404(RutaDeAutobus, id=ruta_id)
    paradas = ParadaDeAutobus.objects.all()
    if request.method == 'POST':
        parada_id = request.POST.get('parada_id')
        parada = get_object_or_404(ParadaDeAutobus, id=parada_id)

        try:
            asociacion = AsociacionParadaRuta(parada=parada, ruta=ruta)
            asociacion.save()
            success_message = 'Parada asociada con éxito a la ruta.'
        except Exception as e:
            messages.error(request, f'Error al asociar la parada: {e}')

        #return redirect('login')  # Puedes redirigir a la página de asociación.

    paradas_disponibles = ParadaDeAutobus.objects.exclude(asociacionparadaruta__ruta=ruta)
    return render(request, 'Sistema/asociar.html', {'ruta': ruta, 'paradas_disponibles': paradas_disponibles,'paradas': paradas, 'success_message': success_message})

def consultar_paradas(request):
    paradas = ParadaDeAutobus.objects.all()
    return render(request, 'Sistema/consultar_paradas.html', {'paradas': paradas})


def consultar_paradas_en_ruta(request, route_id):
    ruta = get_object_or_404(RutaDeAutobus, id=route_id)
    paradas = ParadaDeAutobus.objects.filter(asociacionparadaruta__ruta=ruta)
    
    return render(request, 'Sistema/consulta_paradas.html', {'paradas': paradas})

def consultar_rutas_de_autobus(request):
    rutas = RutaDeAutobus.objects.all()
    rutas_data = []

    for ruta in rutas:
        rutas_data.append({
            'id': ruta.id,
            'nombre': ruta.nombre,
            'origen': ruta.origen,
            'destino': ruta.destino,
            # Agrega más campos según tus necesidades
        })

    return JsonResponse(rutas_data, safe=False)

def detalle_ruta(request, ruta_id):
    ruta = get_object_or_404(RutaDeAutobus, id=ruta_id)
    return render(request, 'Sistema/detalle_ruta.html', {'ruta': ruta})

def detalle_ruta_j(request, ruta_id):
    ruta = get_object_or_404(RutaDeAutobus, id=ruta_id)
    
    # Supongamos que deseas devolver detalles específicos de la ruta en formato JSON.
    ruta_data = {
        'id': ruta.id,
        'nombre': ruta.nombre,
        'origen': ruta.origen,
        'destino': ruta.destino,
        # Agrega más campos según tus necesidades
    }
    
    return JsonResponse(ruta_data, safe=False)

def listar_rutas(request):
    rutas = RutaDeAutobus.objects.all()  # Obtiene todas las rutas de la base de datos
    return render(request, 'Sistema/rutas.html', {'rutas': rutas})


def listar_rutas_pa(request):
    rutas = RutaDeAutobus.objects.all()  # Obtiene todas las rutas de la base de datos
    return render(request, 'Sistema/rutasPa.html', {'rutas': rutas})


def pasajeros(request):
        return render(request, 'Sistema/pasajero.html')


def panel(request):
        return render(request, 'Sistema/dashAdmi.html')


    